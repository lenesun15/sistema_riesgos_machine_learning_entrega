const API_URL = "http://127.0.0.1:8000";
const form = document.getElementById("asset-form");
const statusBox = document.getElementById("status");
const resultBox = document.getElementById("result");
const button = document.getElementById("submit-btn");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  statusBox.textContent = "Procesando los datos con el modelo...";
  resultBox.classList.add("hidden");
  const fd = new FormData(form);
  const payload = {
    asset_type: fd.get("asset_type"),
    confidentiality: Number(fd.get("confidentiality")),
    integrity: Number(fd.get("integrity")),
    availability: Number(fd.get("availability")),
    threat_exposure: Number(fd.get("threat_exposure")),
    vulnerability_count: Number(fd.get("vulnerability_count")),
    control_maturity: Number(fd.get("control_maturity")),
    backup_quality: Number(fd.get("backup_quality")),
    internet_exposed: fd.has("internet_exposed"),
    personal_data: fd.has("personal_data")
  };
  try {
    const response = await fetch(`${API_URL}/api/predict`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Error al ejecutar la predicción.");
    statusBox.textContent = "Clasificación completada.";
    const probs = Object.entries(data.class_probabilities)
      .map(([label, value]) => `<li>${label}: ${(value * 100).toFixed(1)}%</li>`).join("");
    resultBox.innerHTML = `<h2>Resultado del modelo</h2>
      <p class="risk">Riesgo estimado: ${data.predicted_risk}</p>
      <p>Probabilidades estimadas por clase:</p><ul>${probs}</ul>
      <p>${data.notice}</p>`;
    resultBox.classList.remove("hidden");
  } catch (error) {
    statusBox.textContent = `No se pudo completar la solicitud: ${error.message}. Comprueba que el backend esté iniciado.`;
  } finally {
    button.disabled = false;
  }
});
