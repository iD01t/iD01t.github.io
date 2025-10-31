document.addEventListener("DOMContentLoaded", async () => {
  const enhanceLandingPage = async () => {
    try {
      const response = await fetch("/data/catalog.json");
      if (!response.ok) {
        console.error("Failed to fetch catalog data.");
        return;
      }
      const catalog = await response.json();

      const bookLink = document.querySelector("a[href*='books.google.com/books?id=']");
      if (!bookLink) {
        return;
      }

      const url = new URL(bookLink.href);
      const bookId = url.searchParams.get("id");

      if (!bookId) {
        return;
      }

      // The catalog is an array of objects, where the second element is an object with ebooks and audiobooks arrays.
      const allBooks = [...(catalog[1].ebooks || []), ...(catalog[1].audiobooks || [])];
      const book = allBooks.find(b => b.id === bookId);

      if (book && book.cover_hd) {
        const ogImage = document.querySelector("meta[property='og:image']");
        if (ogImage) {
          ogImage.content = book.cover_hd;
        }

        const coverImage = document.querySelector(".book-cover img");
        if (coverImage) {
          coverImage.src = book.cover_hd;
        }
      }
    } catch (error) {
      console.error("Error enhancing landing page:", error);
    }
  };

  enhanceLandingPage();
});
