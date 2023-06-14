const { autocomplete } = window['@algolia/autocomplete-js'];
function debouncePromise(fn, time) {
  let timerId = undefined;

  return function debounced(...args) {
    if (timerId) {
      clearTimeout(timerId);
    }

    return new Promise((resolve) => {
      timerId = setTimeout(() => resolve(fn(...args)), time);
    });
  };
}

const debounced = debouncePromise((items) => Promise.resolve(items), 300);

autocomplete({
  container: '#autocomplete',
  placeholder: 'Search for a movie title',
  getSources({ query }) {
    return debounced([{
      sourceId: 'movies',
      getItems() {
        return fetch(
          `/project_test/search?q=${query}`
        )
          .then((response) => response.json())
      },
      templates: {
        item({ item, html }) {
          return html`<div onclick="${() => window.location.href = `/project_test/similarmovies/${item.id}`}">
              <img class="search-img" src="/project_test/${item.id}/poster"/>
              <div class="search-movie-title" >${item.title}</div>
              <div class="search-movie-genres">${item.genres}</div>
              <div class="search-movie-avgRating">
                <span class="card__rate"><i class="icon ion-ios-star"></i></span>
                <span>${item.avgRating}</span>
              </div>
          </div>`;
        },
      },
      getItemInputValue({ item }) {
        return item.title;
      }
    }]);
  },
});