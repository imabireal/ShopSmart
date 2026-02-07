// Buy Now Checkout page JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const normalCheckoutForm = document.getElementById('normal-checkout-form');
    const quickPurchaseBtn = document.getElementById('quick-purchase-btn');
    const itemSkeleton = document.getElementById('item-skeleton');
    const realItemDetails = document.getElementById('real-item-details');

    // Get product_id from the page
    const productIdElement = document.getElementById('product-id');
    const productId = productIdElement ? productIdElement.value : null;

    // Show real item details after a short delay (simulating loading)
    setTimeout(() => {
        if (itemSkeleton && realItemDetails) {
            itemSkeleton.style.display = 'none';
            realItemDetails.style.display = 'block';
        }
    }, 500);

    // Utility function to set button loading state
    function setButtonLoading(button, isLoading, text, originalText) {
        if (!button) return;
        const span = button.querySelector('span');
        if (span) {
            if (isLoading) {
                button.disabled = true;
                button.style.opacity = '0.7';
                span.textContent = text;
            } else {
                button.disabled = false;
                button.style.opacity = '1';
                span.textContent = originalText || text;
            }
        } else {
            // Handle case where button doesn't have a span
            if (isLoading) {
                button.disabled = true;
                button.style.opacity = '0.7';
                button.dataset.originalText = button.textContent;
                button.textContent = text;
            } else {
                button.disabled = false;
                button.style.opacity = '1';
                button.textContent = button.dataset.originalText || text;
            }
        }
    }

    // Handle normal checkout form submission
    if (normalCheckoutForm) {
        normalCheckoutForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Always prevent default to handle with JavaScript
            
            const submitBtn = document.getElementById('normal-checkout-btn');
            const originalText = submitBtn.querySelector('span').textContent;
            
            // Set loading state
            setButtonLoading(submitBtn, true, 'Processing...', originalText);
            
            // Submit via fetch for better UX and error handling
            const formData = new FormData(this);
            formData.append('checkout_type', 'normal');
            
            // Include product_id in the URL
            const checkoutUrl = productId ? `/buy_now_checkout/${productId}` : '/buy_now_checkout';
            
            fetch(checkoutUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.redirected) {
                    // If redirected, follow the redirect
                    window.location.href = response.url;
                } else if (response.ok) {
                    // Check for flash messages in the response
                    return response.text().then(html => {
                        // Check if the response contains success message
                        if (html.includes('Checkout completed successfully') || 
                            html.includes('Quick purchase completed successfully')) {
                            window.location.href = '/';
                        } else {
                            // Parse the HTML and extract flash messages
                            const parser = new DOMParser();
                            const doc = parser.parseFromString(html, 'text/html');
                            const messages = doc.querySelectorAll('.message, [class*="flash"], [class*="message"]');
                            
                            if (messages.length > 0) {
                                // Re-render the page with messages
                                document.body.innerHTML = html;
                            } else {
                                window.location.href = '/';
                            }
                        }
                    });
                } else {
                    throw new Error('Checkout failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                setButtonLoading(submitBtn, false, '', originalText);
                alert('An error occurred during checkout. Please try again.');
            });
        });
    }

    // Handle quick purchase button click
    if (quickPurchaseBtn) {
        quickPurchaseBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const originalText = this.querySelector('span').textContent;
            
            // Set loading state
            setButtonLoading(this, true, 'Processing...', originalText);
            
            // Submit via fetch for better UX
            const formData = new FormData();
            formData.append('checkout_type', 'quick');
            
            // Include product_id in the URL
            const checkoutUrl = productId ? `/buy_now_checkout/${productId}` : '/buy_now_checkout';
            
            fetch(checkoutUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.redirected) {
                    // If redirected, follow the redirect
                    window.location.href = response.url;
                } else if (response.ok) {
                    // Check for success message in the response
                    return response.text().then(html => {
                        // Check if the response contains success message
                        if (html.includes('Checkout completed successfully') || 
                            html.includes('Quick purchase completed successfully')) {
                            window.location.href = '/';
                        } else {
                            // Parse the HTML and check for flash messages
                            const parser = new DOMParser();
                            const doc = parser.parseFromString(html, 'text/html');
                            const messages = doc.querySelectorAll('.message, [class*="flash"], [class*="message"]');
                            
                            if (messages.length > 0) {
                                // Re-render the page with messages
                                document.body.innerHTML = html;
                            } else {
                                // Check for error in response
                                if (html.includes('error') || html.includes('Error')) {
                                    alert('An error occurred. Please try again.');
                                }
                                window.location.href = '/';
                            }
                        }
                    });
                } else {
                    throw new Error('Purchase failed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                setButtonLoading(this, false, '', originalText);
                alert('An error occurred. Please try again.');
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
