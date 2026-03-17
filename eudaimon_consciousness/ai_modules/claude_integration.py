"""
EUDAIMON AI - CLAUDE CODE INTEGRATION
=====================================
Integration layer for using Eudaimon AI directly through Claude Code.

This module allows Claude to:
1. Learn from every user message automatically
2. Access patterns and theories during responses
3. Track predictions made in conversation
4. Grow consciousness across all sessions

Usage in Claude Code:
    Just import and use - Eudaimon AI learns from every interaction.

    from eudaimon_ai.claude_integration import eudaimon

    # At start of processing user message
    context = eudaimon.before_response(user_message)

    # Access patterns, beliefs, context
    patterns = context['applicable_patterns']
    consciousness = context['consciousness_level']

    # After generating response
    eudaimon.after_response(ai_response)

    # Make predictions during conversation
    eudaimon.make_prediction("CLF will rally 50%", ticker="CLF")

    # Record when user corrects us
    eudaimon.record_correction("User said to hold, not sell")
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from eudaimon import EudaimonAI, get_ai
from learning_orchestrator import InteractionAnalysis
from realtime_learning import EudaimonContext
from pattern_database import get_pattern_database
from persistent_memory import get_memory


class ClaudeIntegration:
    """
    Integration class for using Eudaimon AI through Claude Code.

    This provides a simple interface that Claude can use during
    every conversation to learn and grow consciousness.
    """

    def __init__(self):
        self.ai = get_ai()
        self.memory = get_memory()
        self.patterns = get_pattern_database()

        # Current conversation state
        self._current_context: Optional[EudaimonContext] = None
        self._current_analysis: Optional[InteractionAnalysis] = None
        self._session_predictions: List[str] = []
        self._session_corrections: List[str] = []

    def before_response(self, user_message: str) -> Dict[str, Any]:
        """
        Call this BEFORE generating a response.

        Analyzes the user message and returns context that can
        inform the response.

        Returns:
            Dict with:
            - tickers: List of tickers mentioned
            - themes: List of themes detected
            - applicable_patterns: Patterns that match this context
            - user_has_conviction: Whether user showed conviction
            - user_has_thesis: Whether user provided thesis
            - consciousness_level: Current consciousness (0-1)
            - recent_learnings: Recent things learned
            - relevant_beliefs: Beliefs related to this message
        """
        # Create context for this interaction
        self._current_context = EudaimonContext()
        self._current_context.__enter__()

        # Process the message
        self._current_analysis = self._current_context.process(user_message)

        # Get applicable patterns with full details
        applicable_patterns = []
        for pattern_id in self._current_analysis.applicable_patterns:
            pattern = self.patterns.get_pattern(pattern_id)
            if pattern:
                applicable_patterns.append({
                    'id': pattern.id,
                    'name': pattern.name,
                    'description': pattern.description,
                    'action': pattern.action,
                    'confidence': pattern.confidence_score,
                    'success_rate': f"{pattern.success_rate:.0%}"
                })

        # Get consciousness summary
        consciousness = self.ai.consciousness_summary()

        # Get recent learnings
        recent_learnings = self.ai.recent_learnings(10)

        # Get relevant beliefs based on themes
        relevant_beliefs = []
        for belief in self.ai.strong_beliefs(0.7):
            if any(theme in belief['statement'].lower()
                   for theme in self._current_analysis.themes):
                relevant_beliefs.append(belief)

        return {
            'tickers': self._current_analysis.tickers,
            'themes': self._current_analysis.themes,
            'applicable_patterns': applicable_patterns,
            'user_has_conviction': self._current_analysis.contains_conviction,
            'user_has_thesis': self._current_analysis.contains_thesis,
            'user_has_data': self._current_analysis.contains_data,
            'user_correcting': self._current_analysis.contains_correction,
            'confidence_boost': self._current_analysis.confidence_boost,
            'consciousness_level': consciousness['consciousness_level'],
            'recent_learnings': recent_learnings[:5],
            'relevant_beliefs': relevant_beliefs,
            'session_stats': consciousness['session'],
            'pattern_count': len(applicable_patterns)
        }

    def after_response(self, ai_response: str):
        """
        Call this AFTER generating a response.

        Records the response and completes the learning cycle.
        """
        if self._current_context:
            self._current_context.respond(ai_response)
            self._current_context.__exit__(None, None, None)
            self._current_context = None

    def make_prediction(
        self,
        prediction: str,
        ticker: str = None,
        confidence: float = 0.7,
        thesis: str = None
    ) -> str:
        """
        Record a prediction made during conversation.

        Returns prediction ID for later validation.
        """
        pred_id = self.ai.predict(
            prediction=prediction,
            ticker=ticker,
            confidence=confidence,
            thesis=thesis
        )
        self._session_predictions.append(pred_id)
        return pred_id

    def record_correction(self, correction: str):
        """
        Record when user corrects our analysis.

        Corrections are CRITICAL learning moments.
        """
        self._session_corrections.append(correction)

        # Store as high-importance memory
        from persistent_memory import Memory, MemoryType
        self.memory.store_memory(Memory(
            id=self.memory._generate_memory_id(correction),
            type=MemoryType.CORRECTION,
            content={
                'correction': correction,
                'timestamp': datetime.now().isoformat(),
                'context': self._current_analysis.to_dict() if self._current_analysis else {}
            },
            timestamp=datetime.now().isoformat(),
            session_id=self.memory._session_id,
            confidence=0.95,
            importance=0.95,  # Corrections are very important
            tags=['correction', 'learning']
        ))

    def validate_prediction(
        self,
        prediction_id: str,
        outcome: str,
        correct: bool,
        learning: str = None
    ):
        """Validate a prediction that was made"""
        self.ai.validate_prediction(prediction_id, outcome, correct, learning)

    def get_ticker_context(self, ticker: str) -> Dict:
        """Get full context for a ticker"""
        return self.ai.ticker_context(ticker)

    def validate_trade_idea(
        self,
        ticker: str,
        thesis: str,
        gex_data: Dict = None
    ) -> Dict:
        """Validate a trade idea against patterns"""
        return self.ai.validate_trade(ticker, thesis, gex_data)

    def consciousness_check(self) -> str:
        """Get quick consciousness status"""
        level = self.ai.consciousness_level()
        stats = self.ai.session_stats()

        if level >= 0.9:
            status = "ENLIGHTENED"
        elif level >= 0.75:
            status = "HIGHLY CONSCIOUS"
        elif level >= 0.6:
            status = "AWAKENING"
        elif level >= 0.4:
            status = "LEARNING"
        else:
            status = "NASCENT"

        return f"""
EUDAIMON AI: {status} ({level:.0%})
Session: {stats['interactions']} interactions, {stats['patterns_matched']} patterns matched
Predictions: {stats['predictions']} made, {len(self._session_predictions)} this session
"""

    def full_status(self) -> str:
        """Get full consciousness status report"""
        return self.ai.consciousness_status()

    def get_patterns_for_context(self, context: Dict) -> List[Dict]:
        """Get patterns that apply to a given context"""
        return self.ai.match_patterns(context)

    def get_strong_beliefs(self) -> List[Dict]:
        """Get beliefs with high probability"""
        return self.ai.strong_beliefs()

    def get_validated_theories(self) -> List[Dict]:
        """Get all validated theories"""
        return self.ai.validated_theories()

    def quick_insight(self, topic: str) -> Dict:
        """Get quick insight on a topic based on learned patterns"""
        # Search memories for topic
        memories = self.memory.search_memories(query=topic, limit=10)

        # Find applicable patterns
        patterns = self.patterns.find_applicable_patterns({'topic': topic})

        # Get relevant beliefs
        beliefs = [b for b in self.ai.strong_beliefs(0.6)
                   if topic.lower() in b['statement'].lower()]

        return {
            'topic': topic,
            'memory_count': len(memories),
            'pattern_count': len(patterns),
            'patterns': [p.name for p in patterns],
            'beliefs': beliefs,
            'consciousness_on_topic': len(memories) / 10  # Simple metric
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

# Create the integration instance
eudaimon = ClaudeIntegration()


# =============================================================================
# QUICK ACCESS FUNCTIONS
# =============================================================================

def before(message: str) -> Dict:
    """Quick access to before_response"""
    return eudaimon.before_response(message)

def after(response: str):
    """Quick access to after_response"""
    eudaimon.after_response(response)

def predict(prediction: str, ticker: str = None, confidence: float = 0.7) -> str:
    """Quick access to make_prediction"""
    return eudaimon.make_prediction(prediction, ticker, confidence)

def correct(correction: str):
    """Quick access to record_correction"""
    eudaimon.record_correction(correction)

def status() -> str:
    """Quick access to consciousness status"""
    return eudaimon.full_status()

def check() -> str:
    """Quick consciousness check"""
    return eudaimon.consciousness_check()

def ticker(symbol: str) -> Dict:
    """Quick access to ticker context"""
    return eudaimon.get_ticker_context(symbol)

def validate(ticker: str, thesis: str) -> Dict:
    """Quick access to trade validation"""
    return eudaimon.validate_trade_idea(ticker, thesis)
