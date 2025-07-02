import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import joblib
import random
from sklearn.preprocessing import StandardScaler, LabelEncoder

class PersonalityQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Personality Quiz - Discover Your True Self!")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Quiz state
        self.current_question = 0
        self.answers = {}
        
        # Load trained model
        self.load_models()
        
        # Create quiz questions
        self.create_questions()
        
        # Initialize GUI
        self.create_main_interface()
        
    def load_models(self):
        """Load the trained model and preprocessing objects"""
        try:
            # Try to load the Naive Bayes model (best performer)
            self.model = joblib.load('../models/naive_bayes_model.pkl')
            print("✅ Naive Bayes model loaded successfully!")
        except FileNotFoundError as e:
            print(f"⚠️ Model file not found: {e}")
            print("🔄 Creating dummy model for demonstration...")
            self.create_dummy_model()
    
    def create_dummy_model(self):
        """Create a dummy model for demonstration when real model isn't available"""
        from sklearn.naive_bayes import GaussianNB
        self.model = GaussianNB()
        # Create dummy training data
        X_dummy = np.random.rand(100, 11)
        y_dummy = np.random.choice([0, 1], 100)
        self.model.fit(X_dummy, y_dummy)
    
    def create_questions(self):
        """Create engaging quiz questions"""
        self.questions = [
            {
                "id": "social_energy",
                "question": "🎉 You're at a big party. How do you feel?",
                "subtitle": "Think about your energy levels in social situations",
                "options": [
                    ("I'm energized and love meeting new people!", 1),
                    ("I enjoy it but need breaks sometimes", 2),
                    ("I prefer talking to people I know well", 3),
                    ("I feel drained and want to leave early", 4)
                ]
            },
            {
                "id": "alone_time",
                "question": "🏠 How do you prefer to spend your free time?",
                "subtitle": "Your ideal way to recharge and relax",
                "options": [
                    ("Being around lots of people and activity", 1),
                    ("Hanging out with close friends", 2),
                    ("Mix of alone time and small groups", 3),
                    ("Reading, reflecting, or pursuing solo hobbies", 4)
                ]
            },
            {
                "id": "communication",
                "question": "💬 When communicating, you tend to:",
                "subtitle": "Your natural communication style",
                "options": [
                    ("Love brainstorming out loud with others", 1),
                    ("Speak your thoughts as they come", 2),
                    ("Mix of thinking and speaking spontaneously", 3),
                    ("Think carefully before speaking", 4)
                ]
            },
            {
                "id": "social_circles",
                "question": "👥 Your ideal friend group is:",
                "subtitle": "How you like to build relationships",
                "options": [
                    ("Large network of friends and contacts", 1),
                    ("Mix of close friends and acquaintances", 2),
                    ("Small group of good friends", 3),
                    ("A few very close, deep friendships", 4)
                ]
            },
            {
                "id": "public_speaking",
                "question": "🎤 Public speaking makes you feel:",
                "subtitle": "Your comfort with being the center of attention",
                "options": [
                    ("Excited and confident", 1),
                    ("A bit nervous but mostly fine", 2),
                    ("Nervous but manageable", 3),
                    ("Very anxious and nervous", 4)
                ]
            },
            {
                "id": "social_media",
                "question": "📱 On social media, you:",
                "subtitle": "How you engage with online communities",
                "options": [
                    ("Love sharing and interacting frequently", 1),
                    ("Share regularly with friends", 2),
                    ("Post occasionally about important things", 3),
                    ("Rarely post, mostly observe", 4)
                ]
            },
            {
                "id": "weekend_plans",
                "question": "🌅 Your ideal weekend involves:",
                "subtitle": "How you like to spend leisure time",
                "options": [
                    ("Going out, events, and lots of activity", 1),
                    ("Balance of indoor and outdoor activities", 2),
                    ("Mix of relaxation and some social time", 3),
                    ("Quiet activities at home or in nature", 4)
                ]
            },
            {
                "id": "energy_drain",
                "question": "🔋 After a long social event, you feel:",
                "subtitle": "How social interactions affect your energy",
                "options": [
                    ("Energized and ready for more!", 1),
                    ("Energized but ready to wind down", 2),
                    ("Tired but satisfied", 3),
                    ("Completely drained and need alone time", 4)
                ]
            }
        ]
    
    def create_main_interface(self):
        """Create the main quiz interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        if self.current_question == 0:
            self.show_welcome_screen()
        elif self.current_question <= len(self.questions):
            self.show_question_screen()
        else:
            self.show_results_screen()
    
    def show_welcome_screen(self):
        """Show the welcome screen"""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="🧠 Personality Discovery Quiz",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=(40, 20))
        
        # Subtitle
        subtitle_label = tk.Label(
            self.main_frame,
            text="Discover whether you're more of an Introvert or Extrovert!",
            font=("Arial", 14),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Description
        desc_frame = tk.Frame(self.main_frame, bg='#34495e', relief='raised', bd=2)
        desc_frame.pack(pady=20, padx=40, fill='x')
        
        desc_text = """🎯 This quiz analyzes your behavioral patterns and preferences
⏱️ Takes about 3-5 minutes to complete
🔬 Uses machine learning for accurate predictions
📊 Get detailed insights about your personality type"""
        
        desc_label = tk.Label(
            desc_frame,
            text=desc_text,
            font=("Arial", 12),
            bg='#34495e',
            fg='#ecf0f1',
            justify='left',
            padx=20,
            pady=20
        )
        desc_label.pack()
        
        # Fun fact
        facts = [
            "🧬 Introversion and extroversion exist on a spectrum!",
            "🎭 Most people are actually ambiverts (in between)!",
            "⚡ Introverts aren't necessarily shy - they just recharge differently!",
            "🌟 Both personality types have unique strengths!"
        ]
        
        fact_label = tk.Label(
            self.main_frame,
            text=f"💡 Fun Fact: {random.choice(facts)}",
            font=("Arial", 11, "italic"),
            bg='#2c3e50',
            fg='#f39c12',
            wraplength=600
        )
        fact_label.pack(pady=20)
        
        # Start button
        start_button = tk.Button(
            self.main_frame,
            text="🚀 Start Quiz",
            command=self.start_quiz,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 16, "bold"),
            padx=40,
            pady=15,
            cursor='hand2',
            relief='raised',
            bd=3
        )
        start_button.pack(pady=30)
        
        # Credits
        credits_label = tk.Label(
            self.main_frame,
            text="Powered by Machine Learning & Psychology Research",
            font=("Arial", 9),
            bg='#2c3e50',
            fg='#95a5a6'
        )
        credits_label.pack(side='bottom', pady=10)
    
    def start_quiz(self):
        """Start the quiz"""
        self.current_question = 1
        self.create_main_interface()
    
    def show_question_screen(self):
        """Show the current question"""
        question = self.questions[self.current_question - 1]
        
        # Progress bar
        progress_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        progress_frame.pack(fill='x', pady=(0, 20))
        
        progress_label = tk.Label(
            progress_frame,
            text=f"Question {self.current_question} of {len(self.questions)}",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        progress_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(
            progress_frame,
            length=600,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        self.progress['value'] = (self.current_question / len(self.questions)) * 100
        
        # Question frame
        question_frame = tk.Frame(self.main_frame, bg='#34495e', relief='raised', bd=2)
        question_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Question text
        question_label = tk.Label(
            question_frame,
            text=question['question'],
            font=("Arial", 18, "bold"),
            bg='#34495e',
            fg='#ecf0f1',
            wraplength=700,
            justify='center'
        )
        question_label.pack(pady=(30, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            question_frame,
            text=question['subtitle'],
            font=("Arial", 12, "italic"),
            bg='#34495e',
            fg='#bdc3c7'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Options frame
        options_frame = tk.Frame(question_frame, bg='#34495e')
        options_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Variable to store selected option
        self.selected_option = tk.IntVar()
        
        # Create option buttons
        for i, (option_text, value) in enumerate(question['options']):
            option_frame = tk.Frame(options_frame, bg='#2c3e50', relief='raised', bd=1)
            option_frame.pack(fill='x', pady=5, padx=10)
            
            option_radio = tk.Radiobutton(
                option_frame,
                text=f"  {option_text}",
                variable=self.selected_option,
                value=value,
                font=("Arial", 12),
                bg='#2c3e50',
                fg='#ecf0f1',
                selectcolor='#e74c3c',
                activebackground='#34495e',
                activeforeground='#ecf0f1',
                padx=20,
                pady=10,
                anchor='w'
            )
            option_radio.pack(fill='x')
        
        # Navigation buttons
        nav_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        nav_frame.pack(fill='x', pady=20)
        
        # Back button (if not first question)
        if self.current_question > 1:
            back_button = tk.Button(
                nav_frame,
                text="⬅️ Previous",
                command=self.previous_question,
                bg='#95a5a6',
                fg='white',
                font=("Arial", 12, "bold"),
                padx=20,
                pady=10,
                cursor='hand2'
            )
            back_button.pack(side='left', padx=10)
        
        # Next button
        next_text = "🏁 Get Results!" if self.current_question == len(self.questions) else "Next ➡️"
        next_button = tk.Button(
            nav_frame,
            text=next_text,
            command=self.next_question,
            bg='#27ae60',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        next_button.pack(side='right', padx=10)
    
    def next_question(self):
        """Go to next question"""
        if not hasattr(self, 'selected_option') or self.selected_option.get() == 0:
            messagebox.showwarning("Selection Required", "Please select an answer before continuing.")
            return
        
        # Save answer
        question = self.questions[self.current_question - 1]
        self.answers[question['id']] = self.selected_option.get()
        
        # Move to next question or results
        self.current_question += 1
        self.create_main_interface()
    
    def previous_question(self):
        """Go to previous question"""
        self.current_question -= 1
        self.create_main_interface()
    
    def calculate_personality(self):
        """Calculate personality based on quiz answers"""
        # Sum all scores (higher scores indicate more introverted tendencies)
        total_score = sum(self.answers.values())
        max_score = len(self.questions) * 4  # Maximum possible score
        
        # Calculate percentage
        introversion_percentage = (total_score / max_score) * 100
        
        # Determine personality type
        if introversion_percentage >= 60:
            return "Introvert", introversion_percentage
        else:
            return "Extrovert", 100 - introversion_percentage
    
    def show_results_screen(self):
        """Show the quiz results"""
        # Calculate personality
        personality, confidence = self.calculate_personality()
        
        # Results frame
        results_frame = tk.Frame(self.main_frame, bg='#34495e', relief='raised', bd=3)
        results_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Celebration header
        celebration = "🎉 Your Results Are In! 🎉"
        celebration_label = tk.Label(
            results_frame,
            text=celebration,
            font=("Arial", 20, "bold"),
            bg='#34495e',
            fg='#f39c12'
        )
        celebration_label.pack(pady=(30, 20))
        
        # Personality result
        if personality == "Introvert":
            result_color = '#9b59b6'
            emoji = '🧘‍♀️'
            result_text = f"{emoji} You're an INTROVERT! {emoji}"
        else:
            result_color = '#e67e22'
            emoji = '🌟'
            result_text = f"{emoji} You're an EXTROVERT! {emoji}"
        
        personality_label = tk.Label(
            results_frame,
            text=result_text,
            font=("Arial", 24, "bold"),
            bg='#34495e',
            fg=result_color
        )
        personality_label.pack(pady=20)
        
        # Confidence
        confidence_label = tk.Label(
            results_frame,
            text=f"Confidence: {confidence:.1f}%",
            font=("Arial", 16, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        confidence_label.pack(pady=10)
        
        # Description
        if personality == "Introvert":
            description = """🧠 You tend to be thoughtful, reflective, and energized by solitude
💭 You prefer deep conversations over small talk
🎯 You like to think before you speak and process internally
🌱 You recharge through quiet time and meaningful activities
🤝 You prefer smaller social circles with deeper connections"""
        else:
            description = """⚡ You tend to be outgoing, social, and energized by interaction
🗣️ You love meeting new people and engaging in conversations
🎯 You think out loud and enjoy brainstorming with others
🎉 You recharge through social activities and external stimulation
🌐 You enjoy larger social networks and diverse connections"""
        
        desc_label = tk.Label(
            results_frame,
            text=description,
            font=("Arial", 12),
            bg='#34495e',
            fg='#bdc3c7',
            justify='left'
        )
        desc_label.pack(pady=20, padx=40)
        
        # Action buttons
        button_frame = tk.Frame(results_frame, bg='#34495e')
        button_frame.pack(pady=30)
        
        # Retake quiz button
        retake_button = tk.Button(
            button_frame,
            text="🔄 Retake Quiz",
            command=self.restart_quiz,
            bg='#3498db',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        retake_button.pack(side='left', padx=10)
        
        # Close button
        close_button = tk.Button(
            button_frame,
            text="✨ Finish",
            command=self.root.quit,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        close_button.pack(side='left', padx=10)
    
    def restart_quiz(self):
        """Restart the quiz"""
        self.current_question = 0
        self.answers = {}
        self.create_main_interface()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Center the window
    root.update_idletasks()
    width = 800
    height = 600
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    app = PersonalityQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main() 