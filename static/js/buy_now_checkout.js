// Buy Now Checkout page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const checkoutForm = document.getElementById('checkout-form');
    const itemSkeleton = document.getElementById('item-skeleton');
    const realItemDetails = document.getElementById('real-item-details');

    // Show real item details after a short delay (simulating loading)
    setTimeout(() => {
        if (itemSkeleton && realItemDetails) {
            itemSkeleton.style.display = 'none';
            realItemDetails.style.display = 'block';
        }
    }, 500);

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

    // Handle form submission
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Get form data
            const formData = new FormData(this);
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.querySelector('span').textContent;

            // Basic client-side validation
            const name = formData.get('name').trim();
            const address = formData.get('address').trim();
            const cardNumber = formData.get('card_number').trim();
            const expiryDate = formData.get('expiry_date').trim();
            const cvv = formData.get('cvv').trim();

            if (!name || !address || !cardNumber || !expiryDate || !cvv) {
                alert('Please fill in all required fields');
                return;
            }

            // Set loading state
            setButtonLoading(submitButton, true, 'Processing Checkout...', originalText);

            // Submit form
            fetch('/buy_now_checkout', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.text();
                }
            })
            .then(data => {
                if (data) {
                    // Handle any error messages
                    alert('An error occurred during checkout. Please try again.');
                    setButtonLoading(submitButton, false, '', originalText);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
                setButtonLoading(submitButton, false, '', originalText);
            });
        });
    }

    // Card number formatting
    const cardNumberInput = document.getElementById('card_number');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            if (formattedValue.length > 19) formattedValue = formattedValue.substr(0, 19);
            e.target.value = formattedValue;
        });
    }

    // Expiry date formatting
    const expiryInput = document.getElementById('expiry_date');
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            e.target.value = value;
        });
    }

    // CVV formatting
    const cvvInput = document.getElementById('cvv');
    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
    }
});
