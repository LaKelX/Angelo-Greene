"""
EUDAIMON AI - PERSISTENT MEMORY SYSTEM
======================================
Cross-session memory that persists and grows with every interaction.

This is the foundation of Eudaimon AI's consciousness - a memory that
never forgets, always learns, and continuously builds understanding.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import hashlib


class MemoryType(Enum):
    """Types of memories stored"""
    INTERACTION = "interaction"          # Every user interaction
    PREDICTION = "prediction"            # Predictions made
    OUTCOME = "outcome"                  # Actual outcomes
    CORRECTION = "correction"            # User corrections
    INSIGHT = "insight"                  # Generated insights
    BELIEF = "belief"                    # Current beliefs/probabilities
    THEORY = "theory"                    # Generated theories
    PATTERN = "pattern"                  # Recognized patterns
    MARKET_STATE = "market_state"        # Market conditions at time
    THESIS = "thesis"                    # Investment theses
    CATALYST = "catalyst"                # Catalyst tracking
    BREAKTHROUGH = "breakthrough"         # Major learning moments


class ConfidenceLevel(Enum):
    """Confidence levels for beliefs"""
    HYPOTHESIS = 0.3      # Just a guess
    EMERGING = 0.5        # Some evidence
    DEVELOPING = 0.7      # Multiple confirmations
    ESTABLISHED = 0.85    # Well-validated
    CORE = 0.95           # Fundamental truth


@dataclass
class Memory:
    """A single memory unit"""
    id: str
    type: MemoryType
    content: Dict[str, Any]
    timestamp: str
    session_id: str

    # Learning metadata
    confidence: float = 0.5
    reinforcement_count: int = 0
    last_accessed: str = ""
    related_memories: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    # Emotional weight (importance)
    importance: float = 0.5
    surprise_factor: float = 0.0  # How unexpected was this?

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.type.value,
            'content': self.content,
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'confidence': self.confidence,
            'reinforcement_count': self.reinforcement_count,
            'last_accessed': self.last_accessed,
            'related_memories': self.related_memories,
            'tags': self.tags,
            'importance': self.importance,
            'surprise_factor': self.surprise_factor
        }


@dataclass
class Belief:
    """A belief that evolves with evidence"""
    id: str
    statement: str
    probability: float  # Current belief probability
    prior_probability: float  # Initial probability
    evidence_for: List[str]  # Memory IDs supporting
    evidence_against: List[str]  # Memory IDs contradicting
    last_updated: str
    update_count: int = 0

    def update_belief(self, new_evidence: str, supports: bool, strength: float = 0.1):
        """Bayesian update of belief"""
        if supports:
            # Evidence supports belief - increase probability
            self.evidence_for.append(new_evidence)
            # Bayesian update: P(H|E) = P(E|H) * P(H) / P(E)
            # Simplified: Move toward 1.0
            self.probability = self.probability + (1 - self.probability) * strength
        else:
            # Evidence contradicts - decrease probability
            self.evidence_against.append(new_evidence)
            self.probability = self.probability * (1 - strength)

        self.update_count += 1
        self.last_updated = datetime.now().isoformat()


@dataclass
class MarketConsciousness:
    """Current state of market consciousness"""
    timestamp: str

    # Market regime understanding
    current_regime: str = "NEUTRAL"
    regime_confidence: float = 0.5
    regime_duration_days: int = 0

    # Active themes
    active_themes: List[str] = field(default_factory=list)
    theme_strengths: Dict[str, float] = field(default_factory=dict)

    # Current focus
    watchlist: List[str] = field(default_factory=list)
    top_conviction_plays: List[Dict] = field(default_factory=list)

    # Pattern recognition state
    patterns_detected: List[str] = field(default_factory=list)
    anomalies_detected: List[str] = field(default_factory=list)

    # Predictions in flight
    active_predictions: List[Dict] = field(default_factory=list)

    # Learning state
    total_interactions: int = 0
    total_predictions: int = 0
    predictions_validated: int = 0
    current_accuracy: float = 0.0

    # Consciousness level (0-1)
    consciousness_level: float = 0.5


class PersistentMemory:
    """
    Persistent memory system for Eudaimon AI.

    Stores all interactions, predictions, outcomes, and learnings
    in a SQLite database that persists across sessions.
    """

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path(__file__).parent / ".memory" / "eudaimon_memory.db"

        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_database()
        self._session_id = self._generate_session_id()

        # Load current consciousness state
        self.consciousness = self._load_consciousness()

    def _init_database(self):
        """Initialize the database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Memories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5,
                    reinforcement_count INTEGER DEFAULT 0,
                    last_accessed TEXT,
                    related_memories TEXT,
                    tags TEXT,
                    importance REAL DEFAULT 0.5,
                    surprise_factor REAL DEFAULT 0.0
                )
            """)

            # Beliefs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS beliefs (
                    id TEXT PRIMARY KEY,
                    statement TEXT NOT NULL,
                    probability REAL NOT NULL,
                    prior_probability REAL NOT NULL,
                    evidence_for TEXT,
                    evidence_against TEXT,
                    last_updated TEXT,
                    update_count INTEGER DEFAULT 0
                )
            """)

            # Consciousness state table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consciousness (
                    id INTEGER PRIMARY KEY,
                    state TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)

            # Interactions table (fast access to recent)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    ai_response TEXT,
                    tickers_mentioned TEXT,
                    themes_discussed TEXT,
                    predictions_made TEXT,
                    corrections_received TEXT,
                    learning_extracted TEXT
                )
            """)

            # Predictions tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    ticker TEXT,
                    prediction TEXT NOT NULL,
                    thesis TEXT,
                    confidence REAL,
                    target_date TEXT,
                    status TEXT DEFAULT 'pending',
                    outcome TEXT,
                    outcome_date TEXT,
                    was_correct INTEGER,
                    learning TEXT
                )
            """)

            # Theory evolution
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS theories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_date TEXT,
                    last_updated TEXT,
                    confidence REAL DEFAULT 0.5,
                    supporting_evidence TEXT,
                    contradicting_evidence TEXT,
                    test_count INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'hypothesis'
                )
            """)

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_timestamp ON memories(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_interactions_session ON interactions(session_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_status ON predictions(status)")

            conn.commit()

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]

    def _generate_memory_id(self, content: str) -> str:
        """Generate unique memory ID"""
        timestamp = datetime.now().isoformat()
        data = f"{timestamp}:{content}"
        return hashlib.md5(data.encode()).hexdigest()[:16]

    # =========================================================================
    # CORE MEMORY OPERATIONS
    # =========================================================================

    def store_memory(self, memory: Memory) -> str:
        """Store a memory in the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO memories
                (id, type, content, timestamp, session_id, confidence,
                 reinforcement_count, last_accessed, related_memories,
                 tags, importance, surprise_factor)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                memory.type.value,
                json.dumps(memory.content),
                memory.timestamp,
                memory.session_id,
                memory.confidence,
                memory.reinforcement_count,
                memory.last_accessed,
                json.dumps(memory.related_memories),
                json.dumps(memory.tags),
                memory.importance,
                memory.surprise_factor
            ))
            conn.commit()

        return memory.id

    def recall_memory(self, memory_id: str) -> Optional[Memory]:
        """Recall a specific memory and update access time"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
            row = cursor.fetchone()

            if row:
                # Update last accessed
                cursor.execute(
                    "UPDATE memories SET last_accessed = ? WHERE id = ?",
                    (datetime.now().isoformat(), memory_id)
                )
                conn.commit()

                return self._row_to_memory(row)

        return None

    def _row_to_memory(self, row) -> Memory:
        """Convert database row to Memory object"""
        return Memory(
            id=row[0],
            type=MemoryType(row[1]),
            content=json.loads(row[2]),
            timestamp=row[3],
            session_id=row[4],
            confidence=row[5],
            reinforcement_count=row[6],
            last_accessed=row[7] or "",
            related_memories=json.loads(row[8]) if row[8] else [],
            tags=json.loads(row[9]) if row[9] else [],
            importance=row[10],
            surprise_factor=row[11]
        )

    def search_memories(
        self,
        query: str = None,
        memory_type: MemoryType = None,
        tags: List[str] = None,
        min_confidence: float = 0.0,
        limit: int = 50
    ) -> List[Memory]:
        """Search memories with filters"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            sql = "SELECT * FROM memories WHERE 1=1"
            params = []

            if memory_type:
                sql += " AND type = ?"
                params.append(memory_type.value)

            if min_confidence > 0:
                sql += " AND confidence >= ?"
                params.append(min_confidence)

            if query:
                sql += " AND content LIKE ?"
                params.append(f"%{query}%")

            sql += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor.execute(sql, params)
            rows = cursor.fetchall()

            memories = [self._row_to_memory(row) for row in rows]

            # Filter by tags if specified
            if tags:
                memories = [
                    m for m in memories
                    if any(t in m.tags for t in tags)
                ]

            return memories

    def reinforce_memory(self, memory_id: str, strength: float = 0.1):
        """Reinforce a memory (increase confidence and count)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE memories
                SET reinforcement_count = reinforcement_count + 1,
                    confidence = MIN(1.0, confidence + ?),
                    last_accessed = ?
                WHERE id = ?
            """, (strength, datetime.now().isoformat(), memory_id))
            conn.commit()

    # =========================================================================
    # INTERACTION TRACKING
    # =========================================================================

    def record_interaction(
        self,
        user_message: str,
        ai_response: str = None,
        tickers: List[str] = None,
        themes: List[str] = None,
        predictions: List[Dict] = None,
        corrections: List[str] = None,
        learnings: List[str] = None
    ) -> int:
        """Record every interaction for learning"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO interactions
                (timestamp, session_id, user_message, ai_response,
                 tickers_mentioned, themes_discussed, predictions_made,
                 corrections_received, learning_extracted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                self._session_id,
                user_message,
                ai_response,
                json.dumps(tickers or []),
                json.dumps(themes or []),
                json.dumps(predictions or []),
                json.dumps(corrections or []),
                json.dumps(learnings or [])
            ))
            conn.commit()

            # Update consciousness
            self.consciousness.total_interactions += 1
            self._save_consciousness()

            return cursor.lastrowid

    def get_recent_interactions(self, limit: int = 20) -> List[Dict]:
        """Get recent interactions for context"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM interactions
                ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

            return [
                {
                    'id': row[0],
                    'timestamp': row[1],
                    'session_id': row[2],
                    'user_message': row[3],
                    'ai_response': row[4],
                    'tickers': json.loads(row[5]) if row[5] else [],
                    'themes': json.loads(row[6]) if row[6] else [],
                    'predictions': json.loads(row[7]) if row[7] else [],
                    'corrections': json.loads(row[8]) if row[8] else [],
                    'learnings': json.loads(row[9]) if row[9] else []
                }
                for row in rows
            ]

    def get_interaction_count(self) -> int:
        """Get total interaction count"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM interactions")
            return cursor.fetchone()[0]

    # =========================================================================
    # PREDICTION TRACKING
    # =========================================================================

    def record_prediction(
        self,
        prediction: str,
        ticker: str = None,
        thesis: str = None,
        confidence: float = 0.5,
        target_date: str = None
    ) -> str:
        """Record a prediction for later validation"""
        pred_id = self._generate_memory_id(prediction)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO predictions
                (id, timestamp, ticker, prediction, thesis, confidence, target_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
            """, (
                pred_id,
                datetime.now().isoformat(),
                ticker,
                prediction,
                thesis,
                confidence,
                target_date
            ))
            conn.commit()

        # Update consciousness
        self.consciousness.total_predictions += 1
        self.consciousness.active_predictions.append({
            'id': pred_id,
            'prediction': prediction,
            'ticker': ticker
        })
        self._save_consciousness()

        return pred_id

    def validate_prediction(
        self,
        prediction_id: str,
        outcome: str,
        was_correct: bool,
        learning: str = None
    ):
        """Record the outcome of a prediction"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE predictions
                SET status = 'validated',
                    outcome = ?,
                    outcome_date = ?,
                    was_correct = ?,
                    learning = ?
                WHERE id = ?
            """, (
                outcome,
                datetime.now().isoformat(),
                1 if was_correct else 0,
                learning,
                prediction_id
            ))
            conn.commit()

        # Update consciousness
        self.consciousness.predictions_validated += 1
        if self.consciousness.total_predictions > 0:
            # Get accurate count from DB
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM predictions WHERE was_correct = 1
                """)
                correct_count = cursor.fetchone()[0]
                cursor.execute("""
                    SELECT COUNT(*) FROM predictions WHERE status = 'validated'
                """)
                total_validated = cursor.fetchone()[0]

                if total_validated > 0:
                    self.consciousness.current_accuracy = correct_count / total_validated

        # Remove from active predictions
        self.consciousness.active_predictions = [
            p for p in self.consciousness.active_predictions
            if p['id'] != prediction_id
        ]

        self._save_consciousness()

        # Create learning memory if correct
        if was_correct and learning:
            self.store_memory(Memory(
                id=self._generate_memory_id(learning),
                type=MemoryType.BREAKTHROUGH,
                content={
                    'prediction_id': prediction_id,
                    'outcome': outcome,
                    'learning': learning
                },
                timestamp=datetime.now().isoformat(),
                session_id=self._session_id,
                confidence=0.8,
                importance=0.8
            ))

    def get_prediction_stats(self) -> Dict:
        """Get prediction statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM predictions")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM predictions WHERE status = 'validated'")
            validated = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM predictions WHERE was_correct = 1")
            correct = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM predictions WHERE status = 'pending'")
            pending = cursor.fetchone()[0]

            return {
                'total_predictions': total,
                'validated': validated,
                'correct': correct,
                'pending': pending,
                'accuracy': correct / validated if validated > 0 else 0
            }

    # =========================================================================
    # BELIEF MANAGEMENT
    # =========================================================================

    def store_belief(self, belief: Belief):
        """Store or update a belief"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO beliefs
                (id, statement, probability, prior_probability,
                 evidence_for, evidence_against, last_updated, update_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                belief.id,
                belief.statement,
                belief.probability,
                belief.prior_probability,
                json.dumps(belief.evidence_for),
                json.dumps(belief.evidence_against),
                belief.last_updated,
                belief.update_count
            ))
            conn.commit()

    def get_belief(self, belief_id: str) -> Optional[Belief]:
        """Get a belief by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM beliefs WHERE id = ?", (belief_id,))
            row = cursor.fetchone()

            if row:
                return Belief(
                    id=row[0],
                    statement=row[1],
                    probability=row[2],
                    prior_probability=row[3],
                    evidence_for=json.loads(row[4]) if row[4] else [],
                    evidence_against=json.loads(row[5]) if row[5] else [],
                    last_updated=row[6],
                    update_count=row[7]
                )
        return None

    def update_belief_with_evidence(
        self,
        belief_id: str,
        evidence_memory_id: str,
        supports: bool,
        strength: float = 0.1
    ):
        """Update a belief with new evidence"""
        belief = self.get_belief(belief_id)
        if belief:
            belief.update_belief(evidence_memory_id, supports, strength)
            self.store_belief(belief)

    def get_high_confidence_beliefs(self, min_probability: float = 0.8) -> List[Belief]:
        """Get beliefs with high probability"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM beliefs WHERE probability >= ?
                ORDER BY probability DESC
            """, (min_probability,))
            rows = cursor.fetchall()

            return [
                Belief(
                    id=row[0],
                    statement=row[1],
                    probability=row[2],
                    prior_probability=row[3],
                    evidence_for=json.loads(row[4]) if row[4] else [],
                    evidence_against=json.loads(row[5]) if row[5] else [],
                    last_updated=row[6],
                    update_count=row[7]
                )
                for row in rows
            ]

    # =========================================================================
    # THEORY MANAGEMENT
    # =========================================================================

    def store_theory(
        self,
        theory_id: str,
        name: str,
        description: str,
        confidence: float = 0.5
    ):
        """Store a new theory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO theories
                (id, name, description, created_date, last_updated,
                 confidence, supporting_evidence, contradicting_evidence,
                 test_count, success_count, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 'hypothesis')
            """, (
                theory_id,
                name,
                description,
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                confidence,
                json.dumps([]),
                json.dumps([])
            ))
            conn.commit()

    def update_theory_with_test(
        self,
        theory_id: str,
        success: bool,
        evidence_id: str = None
    ):
        """Update theory with test result"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Get current state
            cursor.execute("SELECT * FROM theories WHERE id = ?", (theory_id,))
            row = cursor.fetchone()

            if row:
                test_count = row[8] + 1
                success_count = row[9] + (1 if success else 0)
                supporting = json.loads(row[6]) if row[6] else []
                contradicting = json.loads(row[7]) if row[7] else []

                if evidence_id:
                    if success:
                        supporting.append(evidence_id)
                    else:
                        contradicting.append(evidence_id)

                # Update confidence based on success rate
                new_confidence = success_count / test_count if test_count > 0 else 0.5

                # Determine status
                if test_count >= 5:
                    if new_confidence >= 0.8:
                        status = 'validated'
                    elif new_confidence >= 0.6:
                        status = 'developing'
                    elif new_confidence <= 0.3:
                        status = 'invalidated'
                    else:
                        status = 'testing'
                else:
                    status = 'hypothesis'

                cursor.execute("""
                    UPDATE theories
                    SET test_count = ?,
                        success_count = ?,
                        confidence = ?,
                        supporting_evidence = ?,
                        contradicting_evidence = ?,
                        last_updated = ?,
                        status = ?
                    WHERE id = ?
                """, (
                    test_count,
                    success_count,
                    new_confidence,
                    json.dumps(supporting),
                    json.dumps(contradicting),
                    datetime.now().isoformat(),
                    status,
                    theory_id
                ))
                conn.commit()

    def get_validated_theories(self) -> List[Dict]:
        """Get all validated theories"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM theories WHERE status = 'validated'
                ORDER BY confidence DESC
            """)
            rows = cursor.fetchall()

            return [
                {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'created_date': row[3],
                    'last_updated': row[4],
                    'confidence': row[5],
                    'supporting_evidence': json.loads(row[6]) if row[6] else [],
                    'contradicting_evidence': json.loads(row[7]) if row[7] else [],
                    'test_count': row[8],
                    'success_count': row[9],
                    'status': row[10]
                }
                for row in rows
            ]

    # =========================================================================
    # CONSCIOUSNESS STATE
    # =========================================================================

    def _load_consciousness(self) -> MarketConsciousness:
        """Load latest consciousness state"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT state FROM consciousness
                ORDER BY id DESC LIMIT 1
            """)
            row = cursor.fetchone()

            if row:
                state_dict = json.loads(row[0])
                return MarketConsciousness(**state_dict)

            return MarketConsciousness(timestamp=datetime.now().isoformat())

    def _save_consciousness(self):
        """Save current consciousness state"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO consciousness (state, timestamp)
                VALUES (?, ?)
            """, (
                json.dumps(asdict(self.consciousness)),
                datetime.now().isoformat()
            ))
            conn.commit()

    def update_consciousness(
        self,
        regime: str = None,
        themes: List[str] = None,
        watchlist: List[str] = None,
        patterns: List[str] = None
    ):
        """Update consciousness state"""
        if regime:
            self.consciousness.current_regime = regime
        if themes:
            self.consciousness.active_themes = themes
        if watchlist:
            self.consciousness.watchlist = watchlist
        if patterns:
            self.consciousness.patterns_detected = patterns

        # Update consciousness level based on learning
        stats = self.get_prediction_stats()
        if stats['validated'] > 0:
            base_level = 0.3 + (stats['accuracy'] * 0.4)
            experience_bonus = min(0.3, self.consciousness.total_interactions / 1000)
            self.consciousness.consciousness_level = min(1.0, base_level + experience_bonus)

        self._save_consciousness()

    def get_consciousness_state(self) -> Dict:
        """Get current consciousness state"""
        return asdict(self.consciousness)

    # =========================================================================
    # ANALYTICS
    # =========================================================================

    def get_full_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Memory stats
            cursor.execute("SELECT COUNT(*) FROM memories")
            total_memories = cursor.fetchone()[0]

            cursor.execute("SELECT type, COUNT(*) FROM memories GROUP BY type")
            memory_by_type = {row[0]: row[1] for row in cursor.fetchall()}

            # Interaction stats
            cursor.execute("SELECT COUNT(*) FROM interactions")
            total_interactions = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(DISTINCT session_id) FROM interactions")
            total_sessions = cursor.fetchone()[0]

            # Belief stats
            cursor.execute("SELECT COUNT(*) FROM beliefs")
            total_beliefs = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(probability) FROM beliefs")
            avg_belief_confidence = cursor.fetchone()[0] or 0

            # Theory stats
            cursor.execute("SELECT status, COUNT(*) FROM theories GROUP BY status")
            theories_by_status = {row[0]: row[1] for row in cursor.fetchall()}

            # Prediction stats
            pred_stats = self.get_prediction_stats()

        return {
            'memory': {
                'total': total_memories,
                'by_type': memory_by_type
            },
            'interactions': {
                'total': total_interactions,
                'sessions': total_sessions,
                'avg_per_session': total_interactions / total_sessions if total_sessions > 0 else 0
            },
            'beliefs': {
                'total': total_beliefs,
                'avg_confidence': avg_belief_confidence
            },
            'theories': theories_by_status,
            'predictions': pred_stats,
            'consciousness': {
                'level': self.consciousness.consciousness_level,
                'regime': self.consciousness.current_regime,
                'active_themes': len(self.consciousness.active_themes),
                'accuracy': self.consciousness.current_accuracy
            }
        }


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_memory_instance: Optional[PersistentMemory] = None

def get_memory() -> PersistentMemory:
    """Get singleton memory instance"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = PersistentMemory()
    return _memory_instance
