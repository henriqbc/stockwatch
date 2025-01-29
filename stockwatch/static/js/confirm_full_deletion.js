function confirmDeletion(event) {
    const confirmation = confirm("Are you sure you want to clear your stock list? This action cannot be undone!");
    
    if (!confirmation) {
        event.preventDefault();
    }
}