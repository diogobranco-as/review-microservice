(function () {
  async function loadReviews(productId, containerId) {
    const API_URL = `http://127.0.0.1:8001/v1/entities/${productId}/reviews`;

    try {
      const response = await fetch(API_URL);
      const reviews = await response.json();

      // Get the container by ID
      let container = document.getElementById(containerId);
      if (!container) {
        console.error(`Container with ID "${containerId}" not found.`);
        return;
      }

      container.innerHTML = `
        <div style="border: 1px solid #ddd; padding: 10px; width: 300px;">
          <h2>Reviews</h2>
          <ul id="review-list">
            ${reviews.length > 0
              ? reviews
                  .map(
                    (rev) =>
                      `<li id="review-${rev.id}">
                        <strong>${rev.rating}/5</strong> - ${rev.comment}
                        <button onclick="editReview(${productId}, ${rev.id}, '${rev.comment}', ${rev.rating})">Edit</button>
                        <button onclick="deleteReview(${productId}, ${rev.id})">Delete</button>
                      </li>`
                  )
                  .join("")
              : "<p>No reviews yet.</p>"}
          </ul>
          <form id="review-form">
            <label>Rating (1-5):</label>
            <input type="number" id="review-rating" min="1" max="5" required>
            <label>Comment:</label>
            <input type="text" id="review-comment" required>
            <button type="submit">Submit</button>
          </form>
        </div>
      `;

      // Handle form submission
      document.getElementById("review-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        const rating = document.getElementById("review-rating").value;
        const comment = document.getElementById("review-comment").value;

        const res = await fetch("http://127.0.0.1:8001/v1/reviews", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ entity_id: productId, rating, comment }),
        });

        if (res.ok) {
          loadReviews(productId, containerId); // Reload reviews
        }
      });
    } catch (error) {
      console.error("Error loading reviews:", error);
    }
  }

  async function deleteReview(productId, reviewId) {
    const DELETE_URL = `http://127.0.0.1:8001/v1/entities/${productId}/reviews/${reviewId}`;

    try {
      const res = await fetch(DELETE_URL, { method: "DELETE" });
      if (res.ok) {
        const reviewElement = document.getElementById(`review-${reviewId}`);
        if (reviewElement) {
          reviewElement.remove(); // Remove the review from the DOM
        }
      } else {
        console.error("Failed to delete review");
      }
    } catch (error) {
      console.error("Error deleting review:", error);
    }
  }

  function editReview(productId, reviewId, currentComment, currentRating) {
    const reviewElement = document.getElementById(`review-${reviewId}`);
    if (!reviewElement) return;

    // Replace the review content with an edit form
    reviewElement.innerHTML = `
      <form id="edit-review-form-${reviewId}">
        <label>Rating (1-5):</label>
        <input type="number" id="edit-review-rating-${reviewId}" value="${currentRating}" min="1" max="5" required>
        <label>Comment:</label>
        <input type="text" id="edit-review-comment-${reviewId}" value="${currentComment}" required>
        <button type="submit">Save</button>
        <button type="button" onclick="cancelEdit(${productId}, ${reviewId}, '${currentComment}', ${currentRating})">Cancel</button>
      </form>
    `;

    // Handle the edit form submission
    document
      .getElementById(`edit-review-form-${reviewId}`)
      .addEventListener("submit", async (e) => {
        e.preventDefault();
        const updatedRating = document.getElementById(`edit-review-rating-${reviewId}`).value;
        const updatedComment = document.getElementById(`edit-review-comment-${reviewId}`).value;

        const UPDATE_URL = `http://127.0.0.1:8001/v1/entities/${productId}/reviews/${reviewId}`;

        try {
          const res = await fetch(UPDATE_URL, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ rating: updatedRating, comment: updatedComment }),
          });

          if (res.ok) {
            loadReviews(productId, "review-widget-container"); // Reload reviews
          } else {
            console.error("Failed to update review");
          }
        } catch (error) {
          console.error("Error updating review:", error);
        }
      });
  }

  function cancelEdit(productId, reviewId, originalComment, originalRating) {
    const reviewElement = document.getElementById(`review-${reviewId}`);
    if (!reviewElement) return;

    // Restore the original review content
    reviewElement.innerHTML = `
      <strong>${originalRating}/5</strong> - ${originalComment}
      <button onclick="editReview(${productId}, ${reviewId}, '${originalComment}', ${originalRating})">Edit</button>
      <button onclick="deleteReview(${productId}, ${reviewId})">Delete</button>
    `;
  }

  // Expose functions globally
  window.loadReviews = loadReviews;
  window.deleteReview = deleteReview;
  window.editReview = editReview;
  window.cancelEdit = cancelEdit;
})();
