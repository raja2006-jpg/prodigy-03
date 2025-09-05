document.addEventListener("DOMContentLoaded", () => {
  // ===== About Section Tabs =====
  const tabLinks = document.querySelectorAll(".tab-link");
  const tabContents = document.querySelectorAll(".tab-content");

  tabLinks.forEach(link => {
    link.addEventListener("click", event => {
      const targetId = event.target.getAttribute("data-tab-target");
      tabLinks.forEach(l => l.classList.remove("active-tab"));
      tabContents.forEach(c => c.classList.remove("active-content"));
      event.target.classList.add("active-tab");
      document.querySelector(targetId).classList.add("active-content");
    });
  });

  // ===== Project Filter =====
  const filterBtns = document.querySelectorAll(".filter-btn");
  const projectCards = document.querySelectorAll(".project-card");

  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      // Active state for buttons
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Filtering logic
      const filter = btn.textContent.toLowerCase();
      projectCards.forEach(card => {
        if (filter === "all" || card.dataset.category === filter) {
          card.style.display = "flex";
        } else {
          card.style.display = "none";
        }
      });
    });
  });

  // ===== Theme Toggle =====
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      document.body.classList.toggle("light-mode");
    });
  }

  // ===== Back to Top Button =====
  const backToTop = document.getElementById("backToTop");
  if (backToTop) {
    window.addEventListener("scroll", () => {
      backToTop.style.display = window.scrollY > 400 ? "block" : "none";
    });

    backToTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
});
