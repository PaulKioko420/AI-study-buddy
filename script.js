document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate-btn');
    const loadHistoryBtn = document.getElementById('load-history');
    const studyNotes = document.getElementById('study-notes');
    const flashcardsContainer = document.getElementById('flashcards-container');
    const historyContainer = document.getElementById('history-container');

    generateBtn.addEventListener('click', generateFlashcards);
    loadHistoryBtn.addEventListener('click', loadSavedFlashcards);

    async function generateFlashcards() {
        const text = studyNotes.value.trim();
        
        if (!text) {
            alert('Please paste your study notes first!');
            return;
        }
        
        generateBtn.innerHTML = '<div class="loading"></div> Generating...';
        generateBtn.disabled = true;
        
        try {
            const response = await fetch('/generate-flashcards', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            displayFlashcards(data.flashcards, flashcardsContainer);
            
        } catch (error) {
            console.error('Error generating flashcards:', error);
            alert('Error generating flashcards. Please try again.');
        } finally {
            generateBtn.innerHTML = '<i class="fas fa-robot"></i> Generate Flashcards';
            generateBtn.disabled = false;
        }
    }

    async function loadSavedFlashcards() {
        loadHistoryBtn.innerHTML = '<div class="loading"></div> Loading...';
        loadHistoryBtn.disabled = true;
        
        try {
            const response = await fetch('/get-flashcards');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (data.flashcards.length === 0) {
                historyContainer.innerHTML = '<p class="placeholder">No saved flashcards found.</p>';
            } else {
                displayFlashcards(data.flashcards, historyContainer);
            }
            
        } catch (error) {
            console.error('Error loading saved flashcards:', error);
            alert('Error loading saved flashcards. Please try again.');
        } finally {
            loadHistoryBtn.innerHTML = '<i class="fas fa-history"></i> Load Saved Flashcards';
            loadHistoryBtn.disabled = false;
        }
    }

    function displayFlashcards(flashcards, container) {
        if (flashcards.length === 0) {
            container.innerHTML = '<p class="placeholder">No flashcards to display.</p>';
            return;
        }
        
        container.innerHTML = '';
        
        flashcards.forEach(card => {
            const flashcardEl = document.createElement('div');
            flashcardEl.className = 'flashcard';
            flashcardEl.innerHTML = `
                <div class="flashcard-inner">
                    <div class="flashcard-front">
                        <h3>Question</h3>
                        <p>${card.question}</p>
                        <small>Click to flip</small>
                    </div>
                    <div class="flashcard-back">
                        <h3>Answer</h3>
                        <p>${card.answer}</p>
                        <small>Click to flip back</small>
                    </div>
                </div>
            `;
            
            flashcardEl.addEventListener('click', function() {
                this.classList.toggle('flipped');
            });
            
            container.appendChild(flashcardEl);
        });
    }
});