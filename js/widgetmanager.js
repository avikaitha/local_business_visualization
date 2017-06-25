var Manager;

(function ($) {

  $(function () {
    Manager = new AjaxSolr.Manager({
      // solrUrl: 'http://reuters-demo.tree.ewdev.ca:9090/reuters/'
      // If you are using a local Solr instance with a "reuters" core, use:
      // solrUrl: 'http://localhost:8983/solr/reuters/'
      // If you are using a local Solr instance with a single core, use:
      solrUrl: 'http://localhost:8983/solr/yelp_new/'
    });


    Manager.addWidget(new AjaxSolr.AutocompleteWidget({
      id: 'text',
      target: '#search',
      fields: [ 'name']
    }));

    Manager.init();
    Manager.store.addByValue('q', '*:*');
    Manager.store.addByValue('fq', 'address:*');
    Manager.store.addByValue('fq', 'state:AZ');
    var params = {
      facet: true,
      'facet.field': ['name'],
      'facet.limit': 20,
      'facet.mincount': 1,
      'f.name.facet.limit': 10,
      'f.full_address.facet.limit': 10,
      'json.nl': 'map'
    };
    for (var name in params) {
      Manager.store.addByValue(name, params[name]);
    }
    Manager.doRequest();
  });

  $.fn.showIf = function (condition) {
    if (condition) {
      return this.show();
    }
    else {
      return this.hide();
    }
  }

})(jQuery);
