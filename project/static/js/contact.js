// Contact form handler — async POST to DRF API.
(function() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  const btnSpinner = document.getElementById('btn-spinner');
  const alertEl = document.getElementById('form-alert');

  function showAlert(message, type) {
    alertEl.className = 'mt-3 alert alert-' + type;
    alertEl.textContent = message;
    alertEl.classList.remove('d-none');
  }

  function hideAlert() {
    alertEl.classList.add('d-none');
  }

  function setLoading(loading) {
    submitBtn.disabled = loading;
    btnText.classList.toggle('d-none', loading);
    btnSpinner.classList.toggle('d-none', !loading);
  }

  function getCookie(name) {
    const val = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return val ? val.pop() : '';
  }

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    hideAlert();

    // Client-side validation
    if (!form.checkValidity()) {
      form.classList.add('was-validated');
      return;
    }

    setLoading(true);

    var payload = {
      name: document.getElementById('name').value.trim(),
      email: document.getElementById('email').value.trim(),
      phone: document.getElementById('phone').value.trim(),
      message: document.getElementById('message').value.trim(),
    };
    var sourceEl = document.getElementById('source');
    if (sourceEl && sourceEl.value) {
      payload.message = '[Source: ' + sourceEl.value + ']\n' + payload.message;
    }

    try {
      const res = await fetch('/api/v1/enquiries/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(payload),
      });

      if (res.status === 201) {
        showAlert('Thank you! Your message has been sent. Our team will get back to you shortly.', 'success');
        form.reset();
        form.classList.remove('was-validated');
      } else if (res.status === 429) {
        showAlert('Too many requests. Please wait a moment and try again.', 'warning');
      } else {
        const data = await res.json().catch(function() { return {}; });
        const detail = data.detail || data.message || 'Something went wrong. Please try again.';
        showAlert(detail, 'danger');
      }
    } catch (err) {
      showAlert('Network error. Please check your connection and try again.', 'danger');
    } finally {
      setLoading(false);
    }
  });

  // Real-time validation feedback
  form.querySelectorAll('input, textarea').forEach(function(el) {
    el.addEventListener('blur', function() {
      if (form.classList.contains('was-validated')) {
        el.checkValidity();
      }
    });
  });
})();
