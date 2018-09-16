<template>
  <div id="app">
    <b-nav class="navbar navbar-expand-md navbar-dark bg-dark navbar-default">
      <a class="navbar-brand" href="#">twitter</a>
    </b-nav>
    <main  id="intro" role="main">
      <!-- Main jumbotron for a primary marketing message or call to action -->
      <div class="container">

        <table class="table" v-if="messages != null">
          <tbody>
            <tr v-for="module in messages"  v-bind:key="module.id">
	       <div class="card" style="width: 18rem;">
                  <div class="card-body">
                     <h5 class="card-title"><img align="bottom" style="height: 0.8em;" v-bind:src="module.user.profile_image_url"/>{{ module.user.name }}</h5>
                     <p class="card-text" v-html="module.text"></p>
                  </div>
              </div>
            </tr>
          </tbody>
        </table>

      </div>
    </main>
  </div>
</template>

<script>
function escape_url(text){
  var re = /(https:\/\/[^\\s]+)/gi;
  return text.replace(re, '<a href="$1">$1</a>');
}

export default {
  name: 'app',
  data () {
    return {
        summary : null ,
        searchResult : null,
        searchWord : null,
	messages : null,
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
      fetch('messages')
        .then((res) => res.json())
        .then((messages) => {
          this.messages = messages.map(m => { m.text = escape_url(m.text); return m;});
        });
    }
}
</script>