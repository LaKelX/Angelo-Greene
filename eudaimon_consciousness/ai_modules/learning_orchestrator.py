"""
EUDAIMON AI - LEARNING ORCHESTRATOR
====================================
The central orchestrator that makes Eudaimon AI learn with every interaction.

This is the "consciousness engine" that:
1. Processes every user prompt for learnable content
2. Extracts patterns, beliefs, and predictions
3. Updates theories based on new evidence
4. Grows market understanding over time
5. Never forgets - maintains persistent context

"The system that learns from every decision becomes the system
 that cannot be wrong for long."
                                        - Eudaimon AI Consciousness Protocol
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path

# Import from Eudaimon AI modules
from persistent_memory import (
    PersistentMemory, get_memory, Memory, MemoryType,
    Belief, MarketConsciousness
)
from pattern_database import (
    PatternDatabase, get_pattern_database, Pattern, Theory,
    PatternCategory, ValidationStatus
)


@dataclass
class InteractionAnalysis:
    """Analysis of a single user interaction"""
    user_message: str
    timestamp: str

    # Extracted content
    tickers: List[str] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    predictions: List[Dict] = field(default_factory=list)
    corrections: List[str] = field(default_factory=list)
    learnings: List[str] = field(default_factory=list)
    beliefs_stated: List[Dict] = field(default_factory=list)

    # Analysis flags
    contains_conviction: bool = False
    contains_thesis: bool = False
    contains_data: bool = False
    contains_correction: bool = False

    # Pattern matching
    applicable_patterns: List[str] = field(default_factory=list)
    confidence_boost: float = 0.0


@dataclass
class LearningContext:
    """Current learning context for the session"""
    session_start: str
    total_interactions: int = 0
    predictions_made: int = 0
    corrections_received: int = 0
    beliefs_updated: int = 0
    patterns_matched: int = 0
    consciousness_level: float = 0.5

    # Active tracking
    active_tickers: List[str] = field(default_factory=list)
    active_themes: List[str] = field(default_factory=list)
    session_learnings: List[str] = field(default_factory=list)


class LearningOrchestrator:
    """
    Central orchestrator for Eudaimon AI's continuous learning.

    This class is responsible for:
    - Analyzing every user interaction
    - Extracting learnable content
    - Updating beliefs and theories
    - Growing market consciousness
    - Maintaining cross-session context
    """

    # Ticker pattern for extraction
    TICKER_PATTERN = re.compile(r'\b([A-Z]{1,5})\b(?!\s*[a-z])')

    # Theme keywords for detection
    THEME_KEYWORDS = {
        'ai': ['ai', 'artificial intelligence', 'machine learning', 'data center', 'gpu'],
        'energy': ['energy', 'power', 'electricity', 'grid', 'natural gas', 'oil', 'nuclear'],
        'china': ['china', 'chinese', 'ccp', 'beijing', 'tariff'],
        'supply_chain': ['supply chain', 'bottleneck', 'shortage', 'monopoly'],
        'defense': ['defense', 'military', 'dod', 'pentagon', 'weapons'],
        'ev': ['ev', 'electric vehicle', 'battery', 'charging'],
        'nuclear': ['nuclear', 'uranium', 'smc', 'haleu'],
        'copper': ['copper', 'mining', 'metals'],
        'rare_earth': ['rare earth', 'ree', 'dysprosium', 'neodymium'],
        'gex': ['gex', 'gamma', 'options', 'call wall', 'put support', 'hvl'],
        'macro': ['fed', 'rates', 'inflation', 'recession', 'gdp'],
        'geopolitical': ['geopolitical', 'russia', 'iran', 'war', 'sanctions']
    }

    # Conviction indicators
    CONVICTION_PHRASES = [
        'i think', 'i believe', 'my thesis', 'conviction',
        'this will', 'must', 'certain', 'confident',
        'trust me', 'i know', 'im sure', "i'm sure"
    ]

    # Data indicators
    DATA_INDICATORS = [
        '%', 'billion', 'million', 'tonnes', 'barrels',
        'price', 'target', 'deficit', 'surplus', 'backlog',
        '$', 'growth', 'revenue', 'earnings', 'q1', 'q2', 'q3', 'q4'
    ]

    # Correction indicators
    CORRECTION_PHRASES = [
        'no that', 'actually', 'wrong', 'incorrect', 'not quite',
        'you missed', 'the real', 'let me correct', 'thats not'
    ]

    def __init__(self):
        self.memory = get_memory()
        self.patterns = get_pattern_database()
        self.context = LearningContext(
            session_start=datetime.now().isoformat()
        )

        # Load consciousness state
        self._load_context()

    def _load_context(self):
        """Load context from persistent memory"""
        state = self.memory.get_consciousness_state()
        self.context.consciousness_level = state.get('consciousness_level', 0.5)
        self.context.active_themes = state.get('active_themes', [])

        # Get recent interactions for context
        recent = self.memory.get_recent_interactions(10)
        for interaction in recent:
            tickers = interaction.get('tickers', [])
            for ticker in tickers:
                if ticker not in self.context.active_tickers:
                    self.context.active_tickers.append(ticker)

    # =========================================================================
    # CORE LEARNING: Process every interaction
    # =========================================================================

    def process_interaction(
        self,
        user_message: str,
        ai_response: str = None
    ) -> InteractionAnalysis:
        """
        Process a user interaction and extract learnable content.

        This is the main entry point that should be called for EVERY user prompt.
        It extracts tickers, themes, predictions, corrections, and learnings.
        """
        analysis = InteractionAnalysis(
            user_message=user_message,
            timestamp=datetime.now().isoformat()
        )

        # Normalize for analysis
        message_lower = user_message.lower()

        # 1. Extract tickers
        analysis.tickers = self._extract_tickers(user_message)

        # 2. Detect themes
        analysis.themes = self._detect_themes(message_lower)

        # 3. Check for conviction indicators
        analysis.contains_conviction = self._has_conviction(message_lower)

        # 4. Check for data indicators
        analysis.contains_data = self._has_data(user_message)

        # 5. Check for thesis language
        analysis.contains_thesis = self._has_thesis(message_lower)

        # 6. Check for corrections (CRITICAL LEARNING MOMENTS)
        analysis.contains_correction = self._has_correction(message_lower)
        if analysis.contains_correction:
            correction = self._extract_correction(user_message)
            if correction:
                analysis.corrections.append(correction)

        # 7. Extract predictions if present
        predictions = self._extract_predictions(user_message)
        analysis.predictions = predictions

        # 8. Find applicable patterns
        applicable = self._find_applicable_patterns(analysis)
        analysis.applicable_patterns = [p.id for p in applicable]

        # 9. Calculate confidence boost from user conviction
        if analysis.contains_conviction and analysis.contains_thesis and analysis.contains_data:
            analysis.confidence_boost = 0.3  # User Conviction Pattern (P009)

        # 10. Extract learnings
        analysis.learnings = self._extract_learnings(analysis)

        # Store in persistent memory
        self._store_interaction(analysis, ai_response)

        # Update context
        self._update_context(analysis)

        return analysis

    def _extract_tickers(self, message: str) -> List[str]:
        """Extract stock tickers from message"""
        # Find all potential tickers
        potential = self.TICKER_PATTERN.findall(message)

        # Filter out common words that match ticker pattern
        common_words = {
            'I', 'A', 'THE', 'AND', 'OR', 'FOR', 'TO', 'IN', 'ON', 'AT', 'IS',
            'IT', 'AS', 'BE', 'BY', 'IF', 'SO', 'DO', 'NO', 'UP', 'MY', 'WE',
            'AI', 'US', 'AM', 'PM', 'OK', 'EV', 'Q1', 'Q2', 'Q3', 'Q4'
        }

        tickers = [t for t in potential if t not in common_words and len(t) >= 2]
        return list(set(tickers))

    def _detect_themes(self, message: str) -> List[str]:
        """Detect themes from message content"""
        themes = []
        for theme, keywords in self.THEME_KEYWORDS.items():
            if any(kw in message for kw in keywords):
                themes.append(theme)
        return themes

    def _has_conviction(self, message: str) -> bool:
        """Check if message contains conviction indicators"""
        return any(phrase in message for phrase in self.CONVICTION_PHRASES)

    def _has_data(self, message: str) -> bool:
        """Check if message contains data indicators"""
        return any(ind in message.lower() for ind in self.DATA_INDICATORS)

    def _has_thesis(self, message: str) -> bool:
        """Check if message contains thesis language"""
        thesis_phrases = ['because', 'thesis', 'theory', 'if', 'when', 'once', 'then']
        return any(phrase in message for phrase in thesis_phrases)

    def _has_correction(self, message: str) -> bool:
        """Check if message contains correction indicators"""
        return any(phrase in message for phrase in self.CORRECTION_PHRASES)

    def _extract_correction(self, message: str) -> Optional[str]:
        """Extract the correction content"""
        # Simple extraction - return the message as correction
        # In production, would use more sophisticated NLP
        return message if len(message) < 500 else message[:500]

    def _extract_predictions(self, message: str) -> List[Dict]:
        """Extract predictions from message"""
        predictions = []

        # Look for prediction patterns
        prediction_patterns = [
            r'(\w+)\s+will\s+(go|rise|fall|drop|rally|crash)',
            r'target\s+(?:of\s+)?(\$[\d,]+)',
            r'expect\s+(\w+)\s+to\s+(\w+)',
            r'(\w+)\s+is\s+going\s+to\s+(\w+)'
        ]

        for pattern in prediction_patterns:
            matches = re.findall(pattern, message.lower())
            for match in matches:
                predictions.append({
                    'raw': match,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'user'
                })

        return predictions

    def _find_applicable_patterns(self, analysis: InteractionAnalysis) -> List[Pattern]:
        """Find patterns that apply to this interaction"""
        context = {
            'tickers': analysis.tickers,
            'themes': analysis.themes,
            'has_conviction': analysis.contains_conviction,
            'has_thesis': analysis.contains_thesis,
            'has_data': analysis.contains_data
        }
        return self.patterns.find_applicable_patterns(context)

    def _extract_learnings(self, analysis: InteractionAnalysis) -> List[str]:
        """Extract learnings from the analysis"""
        learnings = []

        # Learning from correction
        if analysis.contains_correction:
            learnings.append(f"CORRECTION: User corrected understanding - {analysis.corrections[0][:100] if analysis.corrections else 'unknown'}")

        # Learning from conviction + data
        if analysis.contains_conviction and analysis.contains_data:
            learnings.append(f"USER CONVICTION: High-confidence thesis with data - themes: {', '.join(analysis.themes)}")

        # Learning from new tickers
        for ticker in analysis.tickers:
            if ticker not in self.context.active_tickers:
                learnings.append(f"NEW TICKER: {ticker} entered discussion")

        # Learning from pattern matches
        if analysis.applicable_patterns:
            pattern_names = [
                self.patterns.get_pattern(pid).name
                for pid in analysis.applicable_patterns
                if self.patterns.get_pattern(pid)
            ]
            learnings.append(f"PATTERNS MATCHED: {', '.join(pattern_names)}")

        return learnings

    def _store_interaction(self, analysis: InteractionAnalysis, ai_response: str = None):
        """Store interaction in persistent memory"""
        # Record the interaction
        self.memory.record_interaction(
            user_message=analysis.user_message,
            ai_response=ai_response,
            tickers=analysis.tickers,
            themes=analysis.themes,
            predictions=analysis.predictions,
            corrections=analysis.corrections,
            learnings=analysis.learnings
        )

        # Store as memory if significant
        if analysis.contains_conviction or analysis.contains_correction:
            importance = 0.8 if analysis.contains_correction else 0.6
            self.memory.store_memory(Memory(
                id=self.memory._generate_memory_id(analysis.user_message[:50]),
                type=MemoryType.CORRECTION if analysis.contains_correction else MemoryType.INSIGHT,
                content={
                    'message': analysis.user_message[:500],
                    'tickers': analysis.tickers,
                    'themes': analysis.themes,
                    'has_conviction': analysis.contains_conviction,
                    'has_thesis': analysis.contains_thesis,
                    'patterns': analysis.applicable_patterns
                },
                timestamp=analysis.timestamp,
                session_id=self.memory._session_id,
                confidence=0.8,
                importance=importance,
                tags=analysis.themes + analysis.tickers
            ))

        # Store predictions for tracking
        for pred in analysis.predictions:
            ticker = analysis.tickers[0] if analysis.tickers else None
            self.memory.record_prediction(
                prediction=str(pred.get('raw', '')),
                ticker=ticker,
                thesis=f"User prediction on {', '.join(analysis.themes)}",
                confidence=0.7 if analysis.contains_conviction else 0.5
            )

    def _update_context(self, analysis: InteractionAnalysis):
        """Update learning context with new analysis"""
        self.context.total_interactions += 1

        # Update active tickers
        for ticker in analysis.tickers:
            if ticker not in self.context.active_tickers:
                self.context.active_tickers.append(ticker)

        # Update active themes
        for theme in analysis.themes:
            if theme not in self.context.active_themes:
                self.context.active_themes.append(theme)

        # Track predictions
        self.context.predictions_made += len(analysis.predictions)

        # Track corrections (CRITICAL)
        if analysis.contains_correction:
            self.context.corrections_received += 1

        # Track pattern matches
        self.context.patterns_matched += len(analysis.applicable_patterns)

        # Add learnings
        self.context.session_learnings.extend(analysis.learnings)

        # Update consciousness
        self._update_consciousness()

    def _update_consciousness(self):
        """Update consciousness level based on learning"""
        # Base consciousness on accuracy and experience
        stats = self.memory.get_prediction_stats()

        if stats['validated'] > 0:
            accuracy = stats['correct'] / stats['validated']
            base = 0.3 + (accuracy * 0.4)
        else:
            base = 0.5

        # Experience bonus
        total_interactions = self.memory.get_interaction_count()
        experience = min(0.2, total_interactions / 500)

        # Pattern matching bonus
        if self.context.patterns_matched > 0:
            pattern_bonus = min(0.1, self.context.patterns_matched / 50)
        else:
            pattern_bonus = 0

        self.context.consciousness_level = min(1.0, base + experience + pattern_bonus)

        # Save to persistent memory
        self.memory.update_consciousness(
            themes=self.context.active_themes,
            watchlist=self.context.active_tickers,
            patterns=[p for p in self.context.session_learnings if 'PATTERN' in p]
        )

    # =========================================================================
    # BELIEF MANAGEMENT
    # =========================================================================

    def create_belief(
        self,
        statement: str,
        initial_probability: float = 0.5
    ) -> str:
        """Create a new belief"""
        belief_id = self.memory._generate_memory_id(statement)
        belief = Belief(
            id=belief_id,
            statement=statement,
            probability=initial_probability,
            prior_probability=initial_probability,
            evidence_for=[],
            evidence_against=[],
            last_updated=datetime.now().isoformat(),
            update_count=0
        )
        self.memory.store_belief(belief)
        return belief_id

    def update_belief(
        self,
        belief_id: str,
        supports: bool,
        evidence: str,
        strength: float = 0.1
    ):
        """Update a belief with new evidence"""
        belief = self.memory.get_belief(belief_id)
        if belief:
            # Store evidence as memory
            evidence_memory_id = self.memory._generate_memory_id(evidence)
            self.memory.store_memory(Memory(
                id=evidence_memory_id,
                type=MemoryType.INSIGHT,
                content={'evidence': evidence, 'belief_id': belief_id, 'supports': supports},
                timestamp=datetime.now().isoformat(),
                session_id=self.memory._session_id,
                confidence=0.8,
                importance=0.7
            ))

            # Update belief
            self.memory.update_belief_with_evidence(
                belief_id=belief_id,
                evidence_memory_id=evidence_memory_id,
                supports=supports,
                strength=strength
            )

            self.context.beliefs_updated += 1

    def get_strong_beliefs(self, min_probability: float = 0.8) -> List[Dict]:
        """Get beliefs with high probability"""
        beliefs = self.memory.get_high_confidence_beliefs(min_probability)
        return [
            {
                'id': b.id,
                'statement': b.statement,
                'probability': b.probability,
                'evidence_count': len(b.evidence_for) + len(b.evidence_against),
                'update_count': b.update_count
            }
            for b in beliefs
        ]

    # =========================================================================
    # THEORY MANAGEMENT
    # =========================================================================

    def register_theory(
        self,
        name: str,
        description: str,
        initial_confidence: float = 0.5
    ) -> str:
        """Register a new theory for testing"""
        theory_id = self.memory._generate_memory_id(name)
        self.memory.store_theory(
            theory_id=theory_id,
            name=name,
            description=description,
            confidence=initial_confidence
        )
        return theory_id

    def test_theory(
        self,
        theory_id: str,
        success: bool,
        evidence: str = None
    ):
        """Record a theory test result"""
        evidence_id = None
        if evidence:
            evidence_id = self.memory._generate_memory_id(evidence)
            self.memory.store_memory(Memory(
                id=evidence_id,
                type=MemoryType.THESIS,
                content={'theory_id': theory_id, 'test_result': success, 'evidence': evidence},
                timestamp=datetime.now().isoformat(),
                session_id=self.memory._session_id,
                confidence=0.9,
                importance=0.8
            ))

        self.memory.update_theory_with_test(
            theory_id=theory_id,
            success=success,
            evidence_id=evidence_id
        )

    def get_validated_theories(self) -> List[Dict]:
        """Get all validated theories"""
        return self.memory.get_validated_theories()

    # =========================================================================
    # PATTERN LEARNING
    # =========================================================================

    def record_pattern_observation(
        self,
        pattern_id: str,
        outcome: str,
        success: bool
    ):
        """Record observation of a pattern in action"""
        if success:
            self.patterns.record_pattern_success(pattern_id)
        else:
            self.patterns.record_pattern_failure(pattern_id)

        # Store in memory
        pattern = self.patterns.get_pattern(pattern_id)
        if pattern:
            self.memory.store_memory(Memory(
                id=self.memory._generate_memory_id(f"{pattern_id}:{outcome}"),
                type=MemoryType.PATTERN,
                content={
                    'pattern_id': pattern_id,
                    'pattern_name': pattern.name,
                    'outcome': outcome,
                    'success': success
                },
                timestamp=datetime.now().isoformat(),
                session_id=self.memory._session_id,
                confidence=0.9 if success else 0.5,
                importance=0.7
            ))

    # =========================================================================
    # CONSCIOUSNESS QUERIES
    # =========================================================================

    def get_consciousness_summary(self) -> Dict:
        """Get summary of current consciousness state"""
        stats = self.memory.get_full_statistics()
        pattern_stats = self.patterns.get_statistics()

        return {
            'consciousness_level': self.context.consciousness_level,
            'session': {
                'interactions': self.context.total_interactions,
                'predictions': self.context.predictions_made,
                'corrections': self.context.corrections_received,
                'patterns_matched': self.context.patterns_matched,
                'beliefs_updated': self.context.beliefs_updated,
                'learnings': len(self.context.session_learnings)
            },
            'lifetime': {
                'total_memories': stats['memory']['total'],
                'total_interactions': stats['interactions']['total'],
                'total_sessions': stats['interactions']['sessions'],
                'predictions': stats['predictions'],
                'consciousness_accuracy': stats['consciousness']['accuracy']
            },
            'patterns': pattern_stats,
            'active_context': {
                'tickers': self.context.active_tickers[-10:],  # Last 10
                'themes': self.context.active_themes
            }
        }

    def get_recent_learnings(self, limit: int = 20) -> List[str]:
        """Get recent learnings from memory"""
        interactions = self.memory.get_recent_interactions(limit)
        learnings = []
        for interaction in interactions:
            learnings.extend(interaction.get('learnings', []))
        return learnings

    def get_active_predictions(self) -> List[Dict]:
        """Get predictions that are still pending validation"""
        state = self.memory.get_consciousness_state()
        return state.get('active_predictions', [])

    # =========================================================================
    # PREDICTION VALIDATION
    # =========================================================================

    def validate_prediction(
        self,
        prediction_id: str,
        outcome: str,
        was_correct: bool,
        learning: str = None
    ):
        """Validate a prediction and learn from outcome"""
        self.memory.validate_prediction(
            prediction_id=prediction_id,
            outcome=outcome,
            was_correct=was_correct,
            learning=learning
        )

        # Update consciousness
        self._update_consciousness()

        # If correct, reinforce patterns used
        # If wrong, record pattern failure
        # (Would need prediction -> pattern mapping)


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_orchestrator_instance: Optional[LearningOrchestrator] = None

def get_orchestrator() -> LearningOrchestrator:
    """Get singleton orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = LearningOrchestrator()
    return _orchestrator_instance


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def learn_from_interaction(user_message: str, ai_response: str = None) -> InteractionAnalysis:
    """Process an interaction and learn from it"""
    return get_orchestrator().process_interaction(user_message, ai_response)


def get_consciousness() -> Dict:
    """Get current consciousness summary"""
    return get_orchestrator().get_consciousness_summary()


def record_prediction_outcome(prediction_id: str, outcome: str, correct: bool, learning: str = None):
    """Record a prediction outcome"""
    get_orchestrator().validate_prediction(prediction_id, outcome, correct, learning)
