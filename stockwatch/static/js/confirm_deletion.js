function confirmDeletion(event) {
    const confirmation = confirm("Are you sure you want to remove this stock?");
    
    if (!confirmation) {
        event.preventDefault();
    }
}