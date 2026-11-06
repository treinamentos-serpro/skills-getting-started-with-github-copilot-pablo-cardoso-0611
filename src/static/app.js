document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      if (!response.ok) {
        throw new Error("Failed to load activities");
      }
      const activities = await response.json();
      const selectedActivity = activitySelect.value;

      // Clear loading message and previously rendered activities (keeps the placeholder option)
      activitiesList.innerHTML = "";
      activitySelect.querySelectorAll("option:not([value=''])").forEach((option) => option.remove());

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        // Participants are added via textContent so user-provided emails are never parsed as HTML
        const participantsSection = document.createElement("div");
        participantsSection.className = "participants-section";

        const participantsTitle = document.createElement("h5");
        participantsTitle.textContent = `Participantes (${details.participants.length})`;
        participantsSection.appendChild(participantsTitle);

        if (details.participants.length === 0) {
          const emptyMessage = document.createElement("p");
          emptyMessage.className = "no-participants";
          emptyMessage.textContent = "Nenhum participante inscrito ainda.";
          participantsSection.appendChild(emptyMessage);
        } else {
          const participantsList = document.createElement("ul");
          participantsList.className = "participants-list";
          participantsList.setAttribute("role", "list");
          details.participants.forEach((email) => {
            const item = document.createElement("li");
            const participantEmail = document.createElement("span");
            participantEmail.textContent = email;
            item.appendChild(participantEmail);

            const deleteButton = document.createElement("button");
            deleteButton.type = "button";
            deleteButton.className = "delete-participant";
            deleteButton.title = `Cancelar inscricao de ${email}`;
            deleteButton.setAttribute("aria-label", `Cancelar inscricao de ${email} em ${name}`);
            deleteButton.innerHTML = `
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none"
                   stroke="currentColor" stroke-width="2" stroke-linecap="round"
                   stroke-linejoin="round" aria-hidden="true" focusable="false">
                <path d="M3 6h18M9 6V3h6v3M5 6l1 15h12l1-15M10 10v7M14 10v7"/>
              </svg>
            `;
            deleteButton.addEventListener("click", async () => {
              deleteButton.disabled = true;
              try {
                const response = await fetch(
                  `/activities/${encodeURIComponent(name)}/signup?email=${encodeURIComponent(email)}`,
                  { method: "DELETE" }
                );
                const result = await response.json();
                if (!response.ok) {
                  messageDiv.textContent = result.detail || "Nao foi possivel cancelar a inscricao.";
                  messageDiv.className = "error";
                  return;
                }
                messageDiv.textContent = "Inscricao cancelada com sucesso.";
                messageDiv.className = "success";
                await fetchActivities();
              } catch (error) {
                messageDiv.textContent = "Nao foi possivel cancelar a inscricao. Tente novamente.";
                messageDiv.className = "error";
                console.error("Error cancelling signup:", error);
              } finally {
                deleteButton.disabled = false;
              }
            });
            item.appendChild(deleteButton);
            participantsList.appendChild(item);
          });
          participantsSection.appendChild(participantsList);
        }

        activityCard.appendChild(participantsSection);
        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
      activitySelect.value = selectedActivity;
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
