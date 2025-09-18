# flashcards.py
# # flashcards.py
# import streamlit as st
# import random
# import time

# class FlashcardSystem:
#     def __init__(self):
#         # Initialize session state variables
#         if 'flashcards' not in st.session_state:
#             st.session_state.flashcards = []
#         if 'current_card_index' not in st.session_state:
#             st.session_state.current_card_index = 0
#         if 'show_answer' not in st.session_state:
#             st.session_state.show_answer = False
#         if 'card_stats' not in st.session_state:
#             st.session_state.card_stats = {}
#         if 'study_mode' not in st.session_state:
#             st.session_state.study_mode = "sequential"
#         if 'card_ratings' not in st.session_state:
#             st.session_state.card_ratings = {}
#         if 'card_feedback' not in st.session_state:
#             st.session_state.card_feedback = {}

#     def add_flashcards(self, qa_pairs):
#         """Add new flashcards to the system"""
#         for i, pair in enumerate(qa_pairs):
#             card_id = f"card_{len(st.session_state.flashcards) + i}"
#             st.session_state.flashcards.append({
#                 'id': card_id,
#                 'question': pair['question'],
#                 'answer': pair['answer'],
#                 'context': pair.get('context', ''),
#                 'source': pair.get('source', ''),
#                 'created_at': time.time()
#             })
#             # Initialize statistics for this card
#             if card_id not in st.session_state.card_stats:
#                 st.session_state.card_stats[card_id] = {
#                     'views': 0,
#                     'correct': 0,
#                     'incorrect': 0,
#                     'last_reviewed': None
#                 }

#     @property
#     def flashcards(self):
#         return st.session_state.get('flashcards', [])

#     @property
#     def card_stats(self):
#         return st.session_state.get('card_stats', {})

#     def get_current_card(self):
#         """Get the current flashcard based on study mode"""
#         if not self.flashcards:
#             return None
            
#         if st.session_state.study_mode == "random":
#             st.session_state.current_card_index = random.randint(0, len(self.flashcards) - 1)
        
#         return self.flashcards[st.session_state.current_card_index]

#     def next_card(self):
#         """Move to the next card"""
#         if self.flashcards:
#             st.session_state.current_card_index = (st.session_state.current_card_index + 1) % len(self.flashcards)
#             st.session_state.show_answer = False

#     def prev_card(self):
#         """Move to the previous card"""
#         if self.flashcards:
#             st.session_state.current_card_index = (st.session_state.current_card_index - 1) % len(self.flashcards)
#             st.session_state.show_answer = False

#     def record_answer(self, card_id, correct):
#         """Record whether the user answered correctly"""
#         if card_id in st.session_state.card_stats:
#             st.session_state.card_stats[card_id]['views'] += 1
#             if correct:
#                 st.session_state.card_stats[card_id]['correct'] += 1
#             else:
#                 st.session_state.card_stats[card_id]['incorrect'] += 1
#             st.session_state.card_stats[card_id]['last_reviewed'] = time.time()

#     def get_stats(self):
#         """Get overall statistics"""
#         total_cards = len(self.flashcards)
#         if total_cards == 0:
#             return {
#                 'total_cards': 0,
#                 'total_reviews': 0,
#                 'correct_rate': 0,
#                 'most_difficult': []
#             }
        
#         total_views = sum(stat['views'] for stat in st.session_state.card_stats.values())
#         total_correct = sum(stat['correct'] for stat in st.session_state.card_stats.values())
        
#         # Calculate difficulty for each card
#         difficulties = []
#         for card_id, stat in st.session_state.card_stats.items():
#             if stat['views'] > 0:
#                 accuracy = stat['correct'] / stat['views'] if stat['views'] > 0 else 0
#                 difficulties.append({
#                     'card_id': card_id,
#                     'accuracy': accuracy,
#                     'views': stat['views']
#                 })
        
#         # Sort by accuracy (lowest first)
#         difficulties.sort(key=lambda x: x['accuracy'])
        
#         return {
#             'total_cards': total_cards,
#             'total_reviews': total_views,
#             'correct_rate': total_correct / total_views if total_views > 0 else 0,
#             'most_difficult': difficulties[:5]  # Top 5 most difficult cards
#         }

#     def reset_progress(self):
#         """Reset all progress and statistics"""
#         st.session_state.card_stats = {}
#         st.session_state.card_ratings = {}
#         for card in self.flashcards:
#             card_id = card['id']
#             st.session_state.card_stats[card_id] = {
#                 'views': 0,
#                 'correct': 0,
#                 'incorrect': 0,
#                 'last_reviewed': None
#             }

#     def display_flashcard_interface(self):
#         """Display the flashcard interface with beautiful UI"""
#         if not self.flashcards:
#             st.info("No flashcards available. Upload a document to generate flashcards.")
#             return
        
#         # Apply custom CSS
#         st.markdown("""
#         <style>
#             .flashcard-container {
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 padding: 2.5rem;
#                 border-radius: 20px;
#                 color: white;
#                 margin: 1.5rem 0;
#                 box-shadow: 0 10px 30px rgba(0,0,0,0.2);
#                 min-height: 250px;
#                 display: flex;
#                 align-items: center;
#                 justify-content: center;
#                 text-align: center;
#             }
#             .flashcard-text {
#                 font-size: 1.4rem;
#                 font-weight: 600;
#                 line-height: 1.5;
#             }
#             .flashcard-button {
#                 background: rgba(255, 255, 255, 0.1) !important;
#                 border: 2px solid rgba(255, 255, 255, 0.3) !important;
#                 color: white !important;
#                 padding: 0.8rem 1.5rem !important;
#                 margin: 0.5rem !important;
#                 border-radius: 15px !important;
#                 transition: all 0.3s ease !important;
#             }
#             .flashcard-button:hover {
#                 background: rgba(255, 255, 255, 0.2) !important;
#                 border-color: rgba(255, 255, 255, 0.5) !important;
#                 transform: translateY(-2px) !important;
#             }
#             .primary-button {
#                 background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
#                 border: none !important;
#             }
#             .secondary-button {
#                 background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important;
#                 border: none !important;
#             }
#             .progress-bar {
#                 background: #e0e0e0;
#                 border-radius: 10px;
#                 height: 12px;
#                 margin: 1.5rem 0;
#             }
#             .progress-fill {
#                 background: linear-gradient(90deg, #ff6b6b 0%, #ee5a24 100%);
#                 height: 100%;
#                 border-radius: 10px;
#                 transition: width 0.5s ease;
#             }
#             .stats-container {
#                 background: rgba(255, 255, 255, 0.1);
#                 padding: 1.5rem;
#                 border-radius: 15px;
#                 margin: 1rem 0;
#             }
#         </style>
#         """, unsafe_allow_html=True)
        
#         current_card = self.get_current_card()
#         if not current_card:
#             return
        
#         # Record that this card was viewed
#         if current_card['id'] in st.session_state.card_stats:
#             st.session_state.card_stats[current_card['id']]['views'] += 1
        
#         # Progress bar
#         progress = ((st.session_state.current_card_index + 1) / len(self.flashcards)) * 100
#         st.markdown(f"""
#         <div class="progress-bar">
#             <div class="progress-fill" style="width: {progress}%;"></div>
#         </div>
#         <p style="text-align: center; color: #666;">Card {st.session_state.current_card_index + 1} of {len(self.flashcards)}</p>
#         """, unsafe_allow_html=True)
        
#         # Score display
#         stats = self.get_stats()
#         st.markdown(f"""
#         <div style="text-align: center; margin-bottom: 1.5rem;">
#             <h3 style="color: #ee5a24; margin: 0;">Score: {stats['correct_rate']*100:.1f}%</h3>
#             <p style="color: #666; margin: 0;">{stats['total_reviews']} reviews</p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Flashcard display
#         st.markdown(f"""
#         <div class="flashcard-container">
#             <div class="flashcard-text">
#                 {current_card['answer'] if st.session_state.show_answer else current_card['question']}
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Flip button
#         col1, col2, col3 = st.columns([1, 2, 1])
#         with col2:
#             if st.session_state.show_answer:
#                 if st.button("Show Question", key="flip_btn", use_container_width=True, 
#                            type="secondary", icon="↶"):
#                     st.session_state.show_answer = False
#                     st.rerun()
#             else:
#                 if st.button("Show Answer", key="flip_btn", use_container_width=True, 
#                            type="primary", icon="↷"):
#                     st.session_state.show_answer = True
#                     st.rerun()
        
#         # Context information (shown only when answer is visible)
#         if st.session_state.show_answer and current_card.get('context'):
#             with st.expander("View Context"):
#                 st.write(current_card['context'])
        
#         # Navigation and rating buttons
#         st.markdown("<br>", unsafe_allow_html=True)
#         col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)
        
#         with col_nav1:
#             if st.button("← Prev", use_container_width=True, icon="⬅"):
#                 self.prev_card()
#                 st.rerun()
        
#         with col_nav2:
#             if st.button("✓ Easy", use_container_width=True, type="primary", icon="✓"):
#                 self.record_answer(current_card['id'], True)
#                 self.next_card()
#                 st.rerun()
        
#         with col_nav3:
#             if st.button("∼ Medium", use_container_width=True, icon="↔"):
#                 self.record_answer(current_card['id'], True)
#                 self.next_card()
#                 st.rerun()
        
#         with col_nav4:
#             if st.button("✗ Hard", use_container_width=True, type="secondary", icon="✗"):
#                 self.record_answer(current_card['id'], False)
#                 self.next_card()
#                 st.rerun()
        
#         with col_nav5:
#             if st.button("Next →", use_container_width=True, icon="➡"):
#                 self.next_card()
#                 st.rerun()

#     def display_stats_dashboard(self):
#         """Display statistics and progress dashboard"""
#         if not self.flashcards:
#             st.info("No flashcards available. Upload a document to generate flashcards.")
#             return
        
#         stats = self.get_stats()
        
#         st.subheader("📊 Study Statistics")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             st.metric("Total Cards", stats['total_cards'])
        
#         with col2:
#             st.metric("Total Reviews", stats['total_reviews'])
        
#         with col3:
#             st.metric("Accuracy", f"{stats['correct_rate']*100:.1f}%" if stats['total_reviews'] > 0 else "N/A")
        
#         # Most difficult cards
#         if stats['most_difficult']:
#             st.subheader("🎯 Most Challenging Cards")
#             for i, difficult_card in enumerate(stats['most_difficult']):
#                 card = next((c for c in self.flashcards if c['id'] == difficult_card['card_id']), None)
#                 if card:
#                     with st.expander(f"#{i+1}: {card['question'][:50]}... (Accuracy: {difficult_card['accuracy']*100:.1f}%)"):
#                         st.write(f"**Question:** {card['question']}")
#                         st.write(f"**Answer:** {card['answer']}")
#                         st.write(f"**Views:** {difficult_card['views']}")
#                         st.write(f"**Accuracy:** {difficult_card['accuracy']*100:.1f}%")
        
#         # Study mode selection
#         st.subheader("⚙️ Study Settings")
#         study_mode = st.radio("Study Mode", ["sequential", "random"], 
#                              index=0 if st.session_state.study_mode == "sequential" else 1,
#                              horizontal=True)
#         if study_mode != st.session_state.study_mode:
#             st.session_state.study_mode = study_mode
#             st.rerun()
        
#         # Reset progress button
#         if st.button("🔄 Reset All Progress", type="secondary", use_container_width=True):
#             st.session_state.current_card_index = 0
#             st.session_state.show_answer = False
#             self.reset_progress()
#             st.success("Progress reset successfully!")
#             st.rerun()
# flashcards.py
import streamlit as st
import random
import time

class FlashcardSystem:
    def __init__(self):
        # Initialize session state variables
        if 'flashcards' not in st.session_state:
            st.session_state.flashcards = []
        if 'current_card_index' not in st.session_state:
            st.session_state.current_card_index = 0
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
        if 'card_stats' not in st.session_state:
            st.session_state.card_stats = {}
        if 'study_mode' not in st.session_state:
            st.session_state.study_mode = "sequential"
        if 'card_ratings' not in st.session_state:
            st.session_state.card_ratings = {}
        if 'card_feedback' not in st.session_state:
            st.session_state.card_feedback = {}

    def add_flashcards(self, qa_pairs):
        """Add new flashcards to the system"""
        for i, pair in enumerate(qa_pairs):
            card_id = f"card_{len(st.session_state.flashcards) + i}"
            st.session_state.flashcards.append({
                'id': card_id,
                'question': pair['question'],
                'answer': pair['answer'],
                'context': pair.get('context', ''),
                'source': pair.get('source', ''),
                'created_at': time.time()
            })
            # Initialize statistics for this card
            if card_id not in st.session_state.card_stats:
                st.session_state.card_stats[card_id] = {
                    'views': 0,
                    'correct': 0,
                    'incorrect': 0,
                    'last_reviewed': None
                }

    @property
    def flashcards(self):
        return st.session_state.get('flashcards', [])

    @property
    def card_stats(self):
        return st.session_state.get('card_stats', {})

    def get_current_card(self):
        """Get the current flashcard based on study mode"""
        if not self.flashcards:
            return None
            
        if st.session_state.study_mode == "random":
            st.session_state.current_card_index = random.randint(0, len(self.flashcards) - 1)
        
        return self.flashcards[st.session_state.current_card_index]

    def next_card(self):
        """Move to the next card"""
        if self.flashcards:
            st.session_state.current_card_index = (st.session_state.current_card_index + 1) % len(self.flashcards)
            st.session_state.show_answer = False

    def prev_card(self):
        """Move to the previous card"""
        if self.flashcards:
            st.session_state.current_card_index = (st.session_state.current_card_index - 1) % len(self.flashcards)
            st.session_state.show_answer = False

    def record_answer(self, card_id, correct):
        """Record whether the user answered correctly"""
        if card_id in st.session_state.card_stats:
            st.session_state.card_stats[card_id]['views'] += 1
            if correct:
                st.session_state.card_stats[card_id]['correct'] += 1
            else:
                st.session_state.card_stats[card_id]['incorrect'] += 1
            st.session_state.card_stats[card_id]['last_reviewed'] = time.time()

    def get_stats(self):
        """Get overall statistics"""
        total_cards = len(self.flashcards)
        if total_cards == 0:
            return {
                'total_cards': 0,
                'total_reviews': 0,
                'correct_rate': 0,
                'most_difficult': []
            }
        
        total_views = sum(stat['views'] for stat in st.session_state.card_stats.values())
        total_correct = sum(stat['correct'] for stat in st.session_state.card_stats.values())
        
        # Calculate difficulty for each card
        difficulties = []
        for card_id, stat in st.session_state.card_stats.items():
            if stat['views'] > 0:
                accuracy = stat['correct'] / stat['views'] if stat['views'] > 0 else 0
                difficulties.append({
                    'card_id': card_id,
                    'accuracy': accuracy,
                    'views': stat['views']
                })
        
        # Sort by accuracy (lowest first)
        difficulties.sort(key=lambda x: x['accuracy'])
        
        return {
            'total_cards': total_cards,
            'total_reviews': total_views,
            'correct_rate': total_correct / total_views if total_views > 0 else 0,
            'most_difficult': difficulties[:5]  # Top 5 most difficult cards
        }

    def reset_progress(self):
        """Reset all progress and statistics"""
        st.session_state.card_stats = {}
        st.session_state.card_ratings = {}
        for card in self.flashcards:
            card_id = card['id']
            st.session_state.card_stats[card_id] = {
                'views': 0,
                'correct': 0,
                'incorrect': 0,
                'last_reviewed': None
            }

    def display_flashcard_interface(self):
        """Display the flashcard interface with beautiful UI"""
        if not self.flashcards:
            st.info("No flashcards available. Upload a document to generate flashcards.")
            return
        
        # Apply custom CSS
        st.markdown("""
        <style>
            .flashcard-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2.5rem;
                border-radius: 20px;
                color: white;
                margin: 1.5rem 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                min-height: 250px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .flashcard-text {
                font-size: 1.4rem;
                font-weight: 600;
                line-height: 1.5;
            }
            .flashcard-button {
                background: rgba(255, 255, 255, 0.1) !important;
                border: 2px solid rgba(255, 255, 255, 0.3) !important;
                color: white !important;
                padding: 0.8rem 1.5rem !important;
                margin: 0.5rem !important;
                border-radius: 15px !important;
                transition: all 0.3s ease !important;
            }
            .flashcard-button:hover {
                background: rgba(255, 255, 255, 0.2) !important;
                border-color: rgba(255, 255, 255, 0.5) !important;
                transform: translateY(-2px) !important;
            }
            .primary-button {
                background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
                border: none !important;
            }
            .secondary-button {
                background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important;
                border: none !important;
            }
            .progress-bar {
                background: #e0e0e0;
                border-radius: 10px;
                height: 12px;
                margin: 1.5rem 0;
            }
            .progress-fill {
                background: linear-gradient(90deg, #ff6b6b 0%, #ee5a24 100%);
                height: 100%;
                border-radius: 10px;
                transition: width 0.5s ease;
            }
            .stats-container {
                background: rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                border-radius: 15px;
                margin: 1rem 0;
            }
        </style>
        """, unsafe_allow_html=True)
        
        current_card = self.get_current_card()
        if not current_card:
            return
        
        # Record that this card was viewed
        if current_card['id'] in st.session_state.card_stats:
            st.session_state.card_stats[current_card['id']]['views'] += 1
        
        # Progress bar
        progress = ((st.session_state.current_card_index + 1) / len(self.flashcards)) * 100
        st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
        <p style="text-align: center; color: #666;">Card {st.session_state.current_card_index + 1} of {len(self.flashcards)}</p>
        """, unsafe_allow_html=True)
        
        # Score display
        stats = self.get_stats()
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h3 style="color: #ee5a24; margin: 0;">Score: {stats['correct_rate']*100:.1f}%</h3>
            <p style="color: #666; margin: 0;">{stats['total_reviews']} reviews</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Flashcard display
        st.markdown(f"""
        <div class="flashcard-container">
            <div class="flashcard-text">
                {current_card['answer'] if st.session_state.show_answer else current_card['question']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Flip button - FIXED: Use valid emojis
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.show_answer:
                if st.button("Show Question", key="flip_btn", use_container_width=True, 
                           type="secondary"):  # Removed invalid icon
                    st.session_state.show_answer = False
                    st.rerun()
            else:
                if st.button("Show Answer", key="flip_btn", use_container_width=True, 
                           type="primary"):  # Removed invalid icon
                    st.session_state.show_answer = True
                    st.rerun()
        
        # Context information (shown only when answer is visible)
        if st.session_state.show_answer and current_card.get('context'):
            with st.expander("View Context"):
                st.write(current_card['context'])
        
        # Navigation and rating buttons - FIXED: Use valid emojis or no icons
        st.markdown("<br>", unsafe_allow_html=True)
        col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)
        
        with col_nav1:
            if st.button("← Prev", use_container_width=True):  # Removed invalid icon
                self.prev_card()
                st.rerun()
        
        with col_nav2:
            if st.button("✓ Easy", use_container_width=True, type="primary"):  # ✓ is valid
                self.record_answer(current_card['id'], True)
                self.next_card()
                st.rerun()
        
        with col_nav3:
            if st.button("∼ Medium", use_container_width=True):  # Removed invalid icon
                self.record_answer(current_card['id'], True)
                self.next_card()
                st.rerun()
        
        with col_nav4:
            if st.button("✗ Hard", use_container_width=True, type="secondary"):  # ✗ is valid
                self.record_answer(current_card['id'], False)
                self.next_card()
                st.rerun()
        
        with col_nav5:
            if st.button("Next →", use_container_width=True):  # Removed invalid icon
                self.next_card()
                st.rerun()

    def display_stats_dashboard(self):
        """Display statistics and progress dashboard"""
        if not self.flashcards:
            st.info("No flashcards available. Upload a document to generate flashcards.")
            return
        
        stats = self.get_stats()
        
        st.subheader("📊 Study Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Cards", stats['total_cards'])
        
        with col2:
            st.metric("Total Reviews", stats['total_reviews'])
        
        with col3:
            st.metric("Accuracy", f"{stats['correct_rate']*100:.1f}%" if stats['total_reviews'] > 0 else "N/A")
        
        # Most difficult cards
        if stats['most_difficult']:
            st.subheader("🎯 Most Challenging Cards")
            for i, difficult_card in enumerate(stats['most_difficult']):
                card = next((c for c in self.flashcards if c['id'] == difficult_card['card_id']), None)
                if card:
                    with st.expander(f"#{i+1}: {card['question'][:50]}... (Accuracy: {difficult_card['accuracy']*100:.1f}%)"):
                        st.write(f"**Question:** {card['question']}")
                        st.write(f"**Answer:** {card['answer']}")
                        st.write(f"**Views:** {difficult_card['views']}")
                        st.write(f"**Accuracy:** {difficult_card['accuracy']*100:.1f}%")
        
        # Study mode selection
        st.subheader("⚙️ Study Settings")
        study_mode = st.radio("Study Mode", ["sequential", "random"], 
                             index=0 if st.session_state.study_mode == "sequential" else 1,
                             horizontal=True)
        if study_mode != st.session_state.study_mode:
            st.session_state.study_mode = study_mode
            st.rerun()
        
        # Reset progress button
        if st.button("🔄 Reset All Progress", type="secondary", use_container_width=True):  # 🔄 is valid
            st.session_state.current_card_index = 0
            st.session_state.show_answer = False
            self.reset_progress()
            st.success("Progress reset successfully!")
            st.rerun()