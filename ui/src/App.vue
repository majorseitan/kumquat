<template>
  <div id="app">
    <b-nav class="navbar navbar-expand-md navbar-dark bg-dark navbar-default">
      <a class="navbar-brand" href="#">Proof Forge</a>

      <div class="collapse navbar-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="api">rest<span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="graphql">graphql<span class="sr-only">(current)</span></a>
          </li>
        </ul>
      </div>
    </b-nav>
    <main  id="intro" role="main">
      <!-- Main jumbotron for a primary marketing message or call to action -->
      <div class="container">
        <p></p>

        <div class="form-inline">
          <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" id="searchWord">
          <button class="btn my-sm-0" v-on:click="search_keywords">Search</button>
        </div>

        <p></p>

        <p v-if="summary != null && searchResult == null">
          Search
          <span v-if="summary != null">{{ summary.module_count }}</span> modules
          and
          <span v-if="summary != null">{{ summary.declaration_count }}</span> definitions.
        </p>

        <p v-if="searchResult != null">
          Found
          <span v-if="summary != null">{{ searchResult.length }}</span>
          matches
        </p>

        <table class="table" v-if="searchResult != null">
          <thead class="thead-dark">
            <tr>
                <th scope="col">module</th>
                <th scope="col">name</th>
                <th scope="col">expression</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in searchResult" v-bind:key="m.ident">
              <td>{{ m.coq_module }}</td>
              <td>{{ m.ident }}</td>
              <td>{{ m.coq_type }}</td>
            </tr>
          </tbody>
        </table>

        <table class="table" v-if="summary != null && searchResult == null">
          <thead class="thead-dark">
            <tr>
                <th scope="col">module</th>
                <th scope="col">#</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="module in summary.module_index"  v-bind:key="module.coq_module">
              <td>{{ module.coq_module }}</td>
              <th scope="row">{{ module.count }}</th>
            </tr>
          </tbody>
        </table>

      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
        summary : null ,
        searchResult : null,
        searchWord : null
    }
  },
    methods: {
        search_keywords: function () {
            var s = document.getElementById("searchWord").value;
            fetch('proofforge/repository/search?coqEntityId='+s)
                .then((res) => res.json())
                .then((data) => {
                    this.searchResult = data;
                });
            return false;
        }
    },
    created() {
      fetch('proofforge/repository')
        .then((res) => res.json())
        .then((data) => {
          this.summary = data;
        });
    }
}
</script>