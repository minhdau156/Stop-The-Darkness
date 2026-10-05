// Shared quiz widget. Markup contract:
// <div class="quiz" data-correct="1">
//   <p class="q-prompt">...</p>
//   <ul class="q-options">
//     <li><button class="q-opt">...</button></li>  <!-- index 0 -->
//     <li><button class="q-opt">...</button></li>  <!-- index 1 -->
//   </ul>
//   <p class="q-feedback"></p>
// </div>
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".quiz").forEach((quiz) => {
    const correctIndex = parseInt(quiz.dataset.correct, 10);
    const opts = Array.from(quiz.querySelectorAll(".q-opt"));
    const feedback = quiz.querySelector(".q-feedback");
    let answered = false;
    opts.forEach((btn, i) => {
      btn.addEventListener("click", () => {
        if (answered) return;
        answered = true;
        if (i === correctIndex) {
          btn.classList.add("correct");
          feedback.textContent = btn.dataset.rightMsg || "Right.";
          feedback.className = "q-feedback correct";
        } else {
          btn.classList.add("incorrect");
          opts[correctIndex].classList.add("correct");
          feedback.textContent = btn.dataset.wrongMsg || "Not quite — correct answer highlighted.";
          feedback.className = "q-feedback incorrect";
        }
      });
    });
  });
});
