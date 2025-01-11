document.getElementById('quiz-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const answers = {};
    
    formData.forEach((value, key) => {
        answers[key] = value;
    });
    
    // Get name from first question
    const name = answers.q1;
    
    // Send data to server
    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                answers: answers
            })
        });
        
        const data = await response.json();
        
        // Show result modal
        const modal = document.getElementById('result-modal');
        const scoreDisplay = document.getElementById('score-display');
        scoreDisplay.textContent = `You scored ${data.score} out of 100`; // 10 questions * 10 points each
        modal.style.display = 'block';
        
        // Update highest score if necessary
        const currentHighest = parseInt(document.getElementById('highest-score').textContent);
        if (data.score > currentHighest) {
            document.getElementById('highest-score').textContent = data.score;
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Close modal when clicking the X
document.querySelector('.close').addEventListener('click', () => {
    document.getElementById('result-modal').style.display = 'none';
    document.getElementById('quiz-form').reset();
}); 