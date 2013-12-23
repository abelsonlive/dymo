(function() {
  // main script

  var roundFloat = function(amt) {
    // round a float to an int
    return( (Math.round(amt*100)/100).toFixed(0) );
  };

  var iron_number = 0;
  var thatch_number = 0;
  var img_data = {};
  img_data['roofs'] = [];

  $(document).ready(function() {
    
    // pre-populate data labels
    img_data['image'] = $('#img-link').text();
    img_data['number_thatched'] = thatch_number;
    img_data['number_iron'] = iron_number;
    img_data['total'] = thatch_number + iron_number;

    $('#data').val( JSON.stringify(img_data) );

    console.log(img_data);

    $('#clear').click(function() {

        // reset label data
        var iron_number = 0;
        var thatch_number = 0;
        var img_data = {};
        img_data['roofs'] = [];
        img_data['image'] = $('#img-link').text();
        img_data['number_thatched'] = thatch_number;
        img_data['number_iron'] = iron_number;
        img_data['total'] = thatch_number + iron_number;

        // remove markers
        $('.marker').remove();

        // remove logs
        $('#log-list').empty();

        
        console.log(img_data);

    });

    $('#img').click(function(e) {
      
      var offset = $(this).offset();
      
      var x_abs = e.clientX ;
      var y_abs = e.clientY;
      
      var x_img = x_abs - offset.left;
      var y_img = y_abs - offset.top;
      
      var x_display = x_abs - 7;
      var y_display = y_abs -7;
      
      var this_img_type = '';
      var this_roof = {};
      
      if (e.shiftKey) {
        
        iron_number = iron_number + 1;
        this_img_type = 'iron';

        var iron_id = "iron" + iron_number;
        var iron_div = '<div  class="marker" id="' + 
                       iron_id + 
                       '" style="background-color:#a7b0ad; height:10px; width:10px; z-index:1; border: 2px solid;"></div>';

        var iron_log = '<li><span style="background-color:#a7b0ad;"><strong>iron</strong></span>\t<strong>x:</strong> ' + 
                        roundFloat(x_img) + 
                        ', <strong>y:</strong> ' +  
                        roundFloat(y_img) + 
                        '</li>' 

        $(document.body).append(iron_div);
        $("#" + iron_id).css('position', 'absolute');
        $("#" + iron_id).css('top', y_display);
        $("#" + iron_id).css('left', x_display);
        $('#log-list').append(iron_log); 

      } else {

        thatch_number = thatch_number + 1;
        this_img_type = 'thatched';

        var thatch_id = "thatch" + thatch_number;
        var thatch_div = '<div class="marker" id="' + 
                          thatch_id + 
                          '" style="background-color:#788854; height:10px; width:10px; z-index:1; border: 2px solid;"></div>';
        var thatch_log = '<li><span style="background-color:#788854;"> <strong>thatch</strong></span>\t<strong>x:</strong> ' + 
                         roundFloat(x_img) + 
                         ', <strong>y:</strong> ' +  
                         roundFloat(y_img) + '</li>'    

        $(document.body).append(thatch_div);
        $("#" + thatch_id).css('position', 'absolute');
        $("#" + thatch_id).css('top', y_display);
        $("#" + thatch_id).css('left', x_display);
        $('#log-list').append(thatch_log);
        
      }
      // update metadata for image
      img_data['image'] = $('#img-link').text();
      img_data['number_thatched'] = thatch_number;
      img_data['number_iron'] = iron_number;
      img_data['total'] = thatch_number + iron_number;

      // record data for this roof
      this_roof['x'] = x_img;
      this_roof['y'] = y_img;
      this_roof['type'] = this_img_type;
      img_data['roofs'].push(this_roof);

      // update data input field
      $('#data').val( JSON.stringify(img_data) );

      console.log(img_data);

    });
  });
}).call(this);