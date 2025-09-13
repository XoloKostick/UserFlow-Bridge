
document.addEventListener('DOMContentLoaded', function() {
    console.log('UserFlow Bridge loaded successfully');
    
    let isUpdating = false;
    
    async function updateUserData() {
        if (isUpdating) return;
        
        isUpdating = true;
        try {
            const response = await fetch('/api/users');
            const users = await response.json();
            
        
            const countElement = document.querySelector('.count-number');
            if (countElement) {
                countElement.textContent = users.length;
            }
            
            console.log('Data updated successfully', users);
            
        } catch (error) {
            console.error('Error updating data:', error);
        } finally {
            isUpdating = false;
        }
    }
    
   
    setTimeout(updateUserData, 2000);
    
   
    setInterval(updateUserData, 10000);
    
});