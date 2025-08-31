// static/script.js

document.addEventListener('DOMContentLoaded', () => {
  // Cache DOM elements
  const form            = document.getElementById('upload-form');
  const fileInput       = document.getElementById('file-input');
  const merchantSelect  = document.getElementById('merchant');
  const thresholdSlider = document.getElementById('threshold');
  const thresholdValue  = document.getElementById('threshold-value');
  const resultsDiv      = document.getElementById('results');
  const spinner         = document.getElementById('loading-spinner');

  // --- Slider initialization (if present) ---
  if (thresholdSlider && thresholdValue) {
    // set initial value
    thresholdValue.textContent = parseFloat(thresholdSlider.value).toFixed(2);
    // update live
    thresholdSlider.addEventListener('input', () => {
      thresholdValue.textContent = parseFloat(thresholdSlider.value).toFixed(2);
    });
  }

  // --- Merchant dropdown custom validation ---
  if (merchantSelect) {
    merchantSelect.addEventListener('invalid', () => {
      merchantSelect.setCustomValidity('Please select a merchant.');
    });
    merchantSelect.addEventListener('input', () => {
      merchantSelect.setCustomValidity('');
    });
  }

  // --- Form submission via AJAX ---
  if (form) {
    form.addEventListener('submit', handleSubmit);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    clearResults();

    // client-side checks
    if (!fileInput || fileInput.files.length === 0) {
      return showError('Please select a CSV file first.');
    }
    if (thresholdSlider) {
      const v = parseFloat(thresholdSlider.value);
      if (isNaN(v) || v < 0 || v > 1) {
        return showError('Threshold must be between 0 and 1.');
      }
    }

    showSpinner();
    try {
      const payload = await postFormData('/predict');
      if (payload.error) {
        showError(payload.error);
      } else {
        renderTable(payload);
      }
    } catch (err) {
      showError(err.message || 'Unexpected error occurred.');
    } finally {
      hideSpinner();
    }
  }

  // --- Helpers ---

  function clearResults() {
    if (resultsDiv) resultsDiv.innerHTML = '';
  }

  function showSpinner() {
    if (spinner) spinner.style.display = 'block';
    toggleSubmitButton(true);
  }

  function hideSpinner() {
    if (spinner) spinner.style.display = 'none';
    toggleSubmitButton(false);
  }

  function toggleSubmitButton(disable) {
    if (!form) return;
    const btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = disable;
  }

  function showError(msg) {
    clearResults();
    if (!resultsDiv) return;
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger mt-3';
    alert.textContent = msg;
    resultsDiv.appendChild(alert);
  }

  async function postFormData(url) {
    const data = new FormData(form);
    const resp = await fetch(url, { method: 'POST', body: data });
    if (!resp.ok) {
      throw new Error(`Server error: ${resp.status} ${resp.statusText}`);
    }
    return resp.json();
  }

  function renderTable(rows) {
    if (!resultsDiv || !Array.isArray(rows) || rows.length === 0) {
      return showError('No results returned from server.');
    }

    // build table
    const table = document.createElement('table');
    table.className = 'table table-striped table-bordered mt-3';

    // header
    const thead = document.createElement('thead');
    thead.className = 'thead-dark';
    thead.innerHTML = `
      <tr>
        <th>#</th>
        <th>Score</th>
        <th>Prediction</th>
      </tr>`;
    table.appendChild(thead);

    // body
    const tbody = document.createElement('tbody');
    rows.forEach(({ index, score, prediction }) => {
      const tr = document.createElement('tr');
      tr.classList.add(prediction === 1 ? 'table-danger' : 'table-success');
      tr.innerHTML = `
        <th scope="row">${index}</th>
        <td>${score.toFixed(3)}</td>
        <td><strong>${prediction}</strong></td>
      `;
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    resultsDiv.appendChild(table);
  }
});
