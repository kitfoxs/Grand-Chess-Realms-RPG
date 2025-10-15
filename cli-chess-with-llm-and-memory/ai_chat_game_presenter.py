"""
AI Chat Game Presenter
Enhanced offline game that includes LLM chat opponent
"""

from cli_chess.core.game.offline_game import OfflineGameModel, OfflineGamePresenter
from cli_chess.utils import log, threaded
from typing import Optional
import chess


class AIChatGamePresenter(OfflineGamePresenter):
    """
    Enhanced offline game presenter with LLM chat integration.
    The AI opponent chats naturally while using Stockfish for moves.
    """
    
    def __init__(self, model: OfflineGameModel, chat_client=None):
        """
        Initialize AI chat game
        
        Args:
            model: Game model
            chat_client: LMStudioChatClient instance (optional)
        """
        self.chat_client = chat_client
        self.chat_enabled = chat_client is not None
        self.commentary_enabled = True  # User can toggle
        self.pending_chat_response = None
        
        super().__init__(model)
        
        # Initialize chat if available
        if self.chat_enabled:
            try:
                ai_color = "black" if self.model.my_color == chess.WHITE else "white"
                variant = self.model.game_metadata.get("variant", "standard")
                
                greeting = self.chat_client.initialize_game(ai_color, variant)
                if greeting:
                    self._display_chat_message(greeting, is_user=False)
            except Exception as e:
                log.error(f"Error initializing chat: {e}")
                self.chat_enabled = False

    def make_move(self, move: str, is_premove=False) -> None:
        """
        Make user's move and optionally get AI commentary
        
        Args:
            move: Move string
            is_premove: Whether this is a premove
        """
        try:
            if self.model.is_my_turn() and move:
                # Make the move
                self.model.make_move(move)
                
                # Get AI commentary on user's move (async, don't block)
                if self.chat_enabled and self.commentary_enabled:
                    self._comment_on_move_async(move, is_user_move=True)
                
                # Get engine's response move
                self.make_engine_move()
            else:
                self.premove_presenter.set_premove(move)
        except Exception as e:
            if is_premove and isinstance(e, ValueError):
                log.debug("Premove invalid in new position")
            else:
                self.view.alert.show_alert(str(e))

    @threaded
    def make_engine_move(self) -> None:
        """
        Get engine move and present it with AI commentary
        """
        try:
            # Get move from engine
            engine_move = self.engine_presenter.get_best_move()

            if engine_move.resigned:
                log.debug("Engine resigned")
                self.board_presenter.handle_resignation(not self.model.my_color)
                
                # AI comments on resignation
                if self.chat_enabled:
                    msg = self.chat_client.game_over("loss", "resignation")
                    if msg:
                        self._display_chat_message(msg, is_user=False)

            elif engine_move.move:
                move_uci = engine_move.move.uci()
                move_san = self.model.board_model.board.san(engine_move.move)
                
                log.debug(f"Engine move: {move_uci} ({move_san})")
                
                # Make the move
                self.board_presenter.make_move(move_uci)
                
                # AI presents the move with commentary
                if self.chat_enabled and self.commentary_enabled:
                    self._present_move_with_chat(move_san)
                
                # Handle premove
                self.make_move(self.premove_presenter.pop_premove(), is_premove=True)
                
        except Exception as e:
            log.error(e)
            self.view.alert.show_alert(str(e))

    @threaded
    def _comment_on_move_async(self, move: str, is_user_move: bool = True):
        """
        Get AI commentary on a move (runs async)
        
        Args:
            move: Move in SAN/UCI notation
            is_user_move: True if user's move, False if AI's move
        """
        if not self.chat_client:
            return
            
        try:
            fen = self.model.board_model.board.fen()
            
            # Get position evaluation if available
            eval_cp = None
            if hasattr(self.engine_presenter, 'get_evaluation'):
                eval_cp = self.engine_presenter.get_evaluation()
            
            comment = self.chat_client.comment_on_move(
                move, fen, eval_cp, is_user_move
            )
            
            if comment:
                self._display_chat_message(comment, is_user=False)
                
        except Exception as e:
            log.error(f"Error getting move commentary: {e}")

    def _present_move_with_chat(self, move_san: str):
        """
        Present engine's move with AI commentary
        
        Args:
            move_san: Move in SAN notation
        """
        if not self.chat_client:
            return
            
        try:
            fen = self.model.board_model.board.fen()
            
            # Get evaluation
            eval_cp = None
            if hasattr(self.engine_presenter, 'get_evaluation'):
                eval_cp = self.engine_presenter.get_evaluation()
            
            # Get AI's commentary on its own move
            comment = self.chat_client.comment_on_move(
                move_san, fen, eval_cp, is_user_move=False
            )
            
            if comment:
                self._display_chat_message(comment, is_user=False)
                
        except Exception as e:
            log.error(f"Error presenting move with chat: {e}")

    def handle_chat_input(self, message: str) -> None:
        """
        Handle user's chat message or command
        
        Args:
            message: User's message
        """
        if not self.chat_enabled:
            self._display_chat_message("Chat is not available", is_user=False)
            return
        
        message = message.strip()
        
        # Handle commands
        if message.startswith('/'):
            self._handle_chat_command(message[1:].lower())
            return
        
        # Regular chat message
        self._display_chat_message(message, is_user=True)
        self._respond_to_chat_async(message)

    def _handle_chat_command(self, command: str):
        """
        Handle special chat commands
        
        Args:
            command: Command string (without /)
        """
        if command == "hint":
            self._get_hint_async()
        elif command == "explain":
            self._explain_last_move_async()
        elif command == "analyze":
            self._analyze_position_async()
        elif command == "quiet":
            self.commentary_enabled = not self.commentary_enabled
            status = "enabled" if self.commentary_enabled else "disabled"
            self._display_chat_message(f"Commentary {status}", is_user=False)
        elif command == "help":
            help_text = """Commands:
/hint - Get a strategic hint
/explain - Explain AI's last move
/analyze - Analyze current position
/quiet - Toggle commentary on/off
/help - Show this help"""
            self._display_chat_message(help_text, is_user=False)
        else:
            self._display_chat_message(f"Unknown command: /{command}", is_user=False)

    @threaded
    def _respond_to_chat_async(self, message: str):
        """Respond to user's chat message (async)"""
        try:
            response = self.chat_client.respond_to_chat(message)
            if response:
                self._display_chat_message(response, is_user=False)
        except Exception as e:
            log.error(f"Error responding to chat: {e}")

    @threaded
    def _get_hint_async(self):
        """Get hint from AI (async)"""
        try:
            fen = self.model.board_model.board.fen()
            
            # Get top moves from engine
            # This would need engine support for multipv
            best_moves = ["Nf3", "d4", "c4"]  # Placeholder
            
            hint = self.chat_client.provide_hint(fen, best_moves)
            if hint:
                self._display_chat_message(hint, is_user=False)
        except Exception as e:
            log.error(f"Error getting hint: {e}")

    @threaded
    def _explain_last_move_async(self):
        """Get explanation of AI's last move (async)"""
        try:
            move_stack = self.model.board_model.get_move_stack()
            if not move_stack or len(move_stack) < 1:
                self._display_chat_message("No moves to explain yet", is_user=False)
                return
            
            last_move = move_stack[-1]
            fen = self.model.board_model.board.fen()
            
            explanation = self.chat_client.explain_last_move(
                self.model.board_model.board.san(last_move), 
                fen
            )
            if explanation:
                self._display_chat_message(explanation, is_user=False)
        except Exception as e:
            log.error(f"Error explaining move: {e}")

    @threaded
    def _analyze_position_async(self):
        """Get position analysis from AI (async)"""
        try:
            fen = self.model.board_model.board.fen()
            
            # Get evaluation
            eval_cp = 0  # Placeholder
            if hasattr(self.engine_presenter, 'get_evaluation'):
                eval_cp = self.engine_presenter.get_evaluation()
            
            # Get material difference
            material_diff = self._calculate_material_diff()
            
            analysis = self.chat_client.analyze_position(fen, eval_cp, material_diff)
            if analysis:
                self._display_chat_message(analysis, is_user=False)
        except Exception as e:
            log.error(f"Error analyzing position: {e}")

    def _calculate_material_diff(self) -> dict:
        """Calculate material difference"""
        board = self.model.board_model.board
        material = {
            'white': sum([
                len(board.pieces(chess.PAWN, chess.WHITE)),
                len(board.pieces(chess.KNIGHT, chess.WHITE)) * 3,
                len(board.pieces(chess.BISHOP, chess.WHITE)) * 3,
                len(board.pieces(chess.ROOK, chess.WHITE)) * 5,
                len(board.pieces(chess.QUEEN, chess.WHITE)) * 9,
            ]),
            'black': sum([
                len(board.pieces(chess.PAWN, chess.BLACK)),
                len(board.pieces(chess.KNIGHT, chess.BLACK)) * 3,
                len(board.pieces(chess.BISHOP, chess.BLACK)) * 3,
                len(board.pieces(chess.ROOK, chess.BLACK)) * 5,
                len(board.pieces(chess.QUEEN, chess.BLACK)) * 9,
            ])
        }
        material['diff'] = material['white'] - material['black']
        return material

    def _display_chat_message(self, message: str, is_user: bool):
        """
        Display chat message in UI
        
        Args:
            message: Message to display
            is_user: True if from user, False if from AI
        """
        # This would need to be implemented in the view
        # For now, just log it
        prefix = "You" if is_user else "AI"
        log.info(f"[CHAT] {prefix}: {message}")
        
        # If view has chat display method, call it
        if hasattr(self.view, 'display_chat_message'):
            self.view.display_chat_message(message, is_user)

    def _parse_and_present_game_over(self) -> None:
        """Handle game over with AI commentary"""
        super()._parse_and_present_game_over()
        
        # Get AI's reaction to game end
        if self.chat_enabled:
            try:
                result = self.model.game_metadata.game_status
                winner = result.winner if hasattr(result, 'winner') else None
                
                # Determine result from AI's perspective
                ai_color = chess.BLACK if self.model.my_color == chess.WHITE else chess.WHITE
                
                if winner is None:
                    game_result = "draw"
                elif winner == ai_color:
                    game_result = "win"
                else:
                    game_result = "loss"
                
                reason = str(result.status) if hasattr(result, 'status') else "unknown"
                
                msg = self.chat_client.game_over(game_result, reason)
                if msg:
                    self._display_chat_message(msg, is_user=False)
            except Exception as e:
                log.error(f"Error getting game-over commentary: {e}")

    def exit(self) -> None:
        """Clean up on exit"""
        try:
            if self.chat_enabled and self.chat_client:
                self.chat_client.clear_history()
            super().exit()
        except Exception as e:
            log.error(f"Error during exit: {e}")


def start_ai_chat_game(game_parameters: dict, lm_studio_config: dict = None):
    """
    Start an offline game with AI chat opponent
    
    Args:
        game_parameters: Game configuration
        lm_studio_config: LM Studio configuration (optional)
    """
    from cli_chess.utils.ui_common import change_views
    
    # Import here to avoid circular dependency
    # from llm_chat_client import LMStudioChatClient
    
    chat_client = None
    if lm_studio_config and lm_studio_config.get('enabled', False):
        try:
            # Initialize chat client
            # chat_client = LMStudioChatClient(
            #     api_url=lm_studio_config.get('api_url', 'http://localhost:1234/v1'),
            #     model=lm_studio_config.get('model', 'local-model'),
            #     personality=lm_studio_config.get('personality', 'friendly')
            # )
            
            # # Test connection
            # success, message = chat_client.check_connection()
            # if not success:
            #     log.warning(f"LM Studio connection failed: {message}")
            #     chat_client = None
            pass  # Placeholder for actual implementation
        except Exception as e:
            log.error(f"Failed to initialize chat client: {e}")
            chat_client = None
    
    # Start game
    model = OfflineGameModel(game_parameters)
    presenter = AIChatGamePresenter(model, chat_client)
    change_views(presenter.view, presenter.view.input_field_container)
