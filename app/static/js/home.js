// Home page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const buyNowButtons = document.querySelectorAll('.buy-now');
    const loginRequiredButtons = document.querySelectorAll('.login-required');

    // Utility function to set button loading state
    function setButtonLoading(button, isLoading, text, originalText) {
        const span = button.querySelector('span');
        if (isLoading) {
            button.disabled = true;
            button.style.opacity = '0.7';
            span.textContent = text;
        } else {
            button.disabled = false;
            button.style.opacity = '1';
            span.textContent = originalText;
        }
    }

    // Handle add to cart for authenticated users
    addToCartButtons.forEach(button => {
        const originalText = button.querySelector('span').textContent;
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');

            // Set loading state
            setButtonLoading(this, true, 'Adding...', originalText);

            // Send AJAX request to add to cart
            fetch(`/add_to_cart/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update cart count
                    const cartCount = document.getElementById('cart-count');
                    if (cartCount) {
                        cartCount.textContent = data.cart_count;
                        cartCount.classList.remove('hidden');
                    }

                    // Show success state briefly
                    setButtonLoading(this, false, '✓ Added', originalText);
                    setTimeout(() => {
                        setButtonLoading(this, false, '', originalText);
                    }, 800);
                } else {
                    if (data.redirect) {
                        if (confirm(data.message + '. Would you like to log in now?')) {
                            window.location.href = data.redirect;
                        }
                    } else {
                        alert('Error: ' + data.message);
                    }
                    setButtonLoading(this, false, '', originalText);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
                setButtonLoading(this, false, '', originalText);
            });
        });
    });

    // Handle buy now for authenticated users
    buyNowButtons.forEach(button => {
        const originalText = button.querySelector('span').textContent;
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');

            // Set loading state
            setButtonLoading(this, true, 'Processing...', originalText);

            // Small delay to show loading state before redirect
            setTimeout(() => {
                window.location.href = `/buy_now_checkout/${productId}`;
            }, 500);
        });
    });

    // Handle login requirement for non-authenticated users
    loginRequiredButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productName = this.getAttribute('data-product-name');

            // Add a subtle loading effect
            this.style.opacity = '0.7';
            setTimeout(() => {
                this.style.opacity = '1';
                if (confirm(`Please log in to add "${productName}" to your cart. Would you like to log in now?`)) {
                    window.location.href = '/login';
                }
            }, 200);
        });
    });
});
