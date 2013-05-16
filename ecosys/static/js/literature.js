$(function () {

  var format = function (state) {
    return state.text.replace(/\(.*\)/, '');
  };

  $('select[multiple]').select2({
    width: '600px',
    formatSelection: format
  });

  $('.tagit').select2({
    width: '600px',
    tags: [],
    tokenSeparators: []
  });

  $('#spatial').on('change', function () {

    if($(this).val() == '1') {
      $('#spatial_scale').parents('.row').show();
      $('#countries').parents('.row').show();
    } else {
      $('#spatial_scale').parents('.row').hide();
      $('#countries').parents('.row').hide();
    }

  }).change();

  $('#ecosystems').on('change', function () {
    if($(this).val() == '1') {
      $('#ecosystem-types-issues').parents('.row').show();
    } else {
      $('#ecosystem-types-issues').parents('.row').hide();
    }
  }).change();

  $('#ecosystem_services').on('change', function () {
    if($(this).val() == '1') {
      $('#ecosystem-service-types').parents('.row').show();
    } else {
      $('#ecosystem-service-types').parents('.row').hide();
    }
  }).change();


  $('.ecosystem-type-other').on('click', function (e) {
    e.preventDefault();
    var rel = $(this).data('rel');
    var type = $(this).data('type');
    var row = $(rel).find('tbody tr:last');
    var category = prompt('Add another category');
    var fields = ['urban', 'cropland', 'grassland', 'woodland', 'heathland',
                  'vegetated', 'wetland', 'rivers', 'marine'];

    if(!category) return;

    row.find('td').eq(0).append($('<div>').attr({
      'class': 'category-left',
    }).text(category));

    $.each(fields, function (i, value) {
      var parent_html = $('<li>');
      var input = $('<input>').attr({
        'type': 'checkbox',
        'value': category,
        'name': 'ecosystem_types_' + type + '-' + value
      })
      parent_html.append(input);
      row.find('td').eq(i+1).find('ul').append(parent_html);
    });

  });

  $('.ecosystem-service-type-other').on('click', function (e) {
    e.preventDefault();
    var rel = $(this).data('rel');
    var row = $(rel).find('tbody tr:last');
    var category = prompt('Add another category');
    var fields = ['provisioning', 'regulating', 'cultural'];

    if(!category) return;

    row.find('td').eq(0).append($('<div>').attr({
      'class': 'category-left',
    }).text(category));

    $.each(fields, function (i, value) {
      var parent_html = $('<li>')
      var input = $('<input>').attr({
        'type': 'checkbox',
        'value': category,
        'name': 'ecosystem_services_types-' + value
      });
      parent_html.append(input);
      row.find('td').eq(i+1).find('ul').append(parent_html);
    });
  });


  $('.add-object').on('click', function (e) {
    e.preventDefault();

    var title = $(this).data('title');
    var url = $(this).attr('href');
    $('#modal').html('')
    $('#modal').removeData();
    $.get(url, function (data) {
      $('#modal').attr('title', title);
      $('#modal').html(data.html);
      $('#modal').dialog({
        height: 150,
        width: 350,
        modal: true
      });
    });
  });

  $('#modal').on('submit', '#author-form', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var data = $(this).serialize();

    $.post(url, data, function (data) {
      if(data.status == 'success') {
        $('#modal').dialog('close');
        var option = $('<option>').attr({
          'value': data.author.id,
        });
        option.text(data.author.name)
        $('#authors').append(option);

        var values = $('#authors').val() || [];
        values.push(data.author.id);
        $('#authors').val(values).trigger('change');
      } else {
        $('#modal').html(data.html);
      }
    });
  });

  $('#modal').on('submit', '#organisation-form', function (e) {
    e.preventDefault();
    var url = $(this).attr('action');
    var data = $(this).serialize();

    $.post(url, data, function (data) {
      if(data.status == 'success') {
        $('#modal').dialog('close');
        var option = $('<option selected>').attr({
          'value': data.organisation.id,
        });
        option.text(data.organisation.name)
        $('#organisations').append(option);
        var values = $('#organisations').val() || [];
        values.push(data.organisation.id);
        $('#organisations').val(values).trigger('change');
      } else {
        $('#modal').html(data.html);
      }
    });
  });

  $('#resource-delete').on('click', function (e) {
    e.preventDefault();
    if(confirm('Are you sure you want to delete this resource ?')) {
      $.ajax({
        type: 'DELETE',
        url: $(this).attr('href'),
        success: function (data) {
          document.location = data.url;
        }
      })
    }
  });

});
