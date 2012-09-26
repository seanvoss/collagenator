var imgs = {},
compute_image,
promises=[],
imgAspect={},
paper,
fts = [],
matrix={};
url ='http://www.reddit.com/r/aww/hot/.json?limit=100&jsonp=?';
(function($){})(window.jQuery);

/* Trigger when page is ready */
$(document).ready(function (){
	var hero = $('.hero'), 
	    squares = {};
	/* Ask Reddit for the Hottest AWWW Pictures */
	$.getJSON(url,function(response){
		/* Create Deferred Objects */
		var deferreds = $(response.data.children).map(function(){
		if(this.data.url.toLowerCase().indexOf('.jpg')!= -1 || this.data.url.toLowerCase().indexOf('.png')!= -1 ){
			$('article:first').clone(false).html('<img id="'+
			this.data.id+'" class="thumb" src="'+
			this.data.thumbnail+'" />').prependTo($('article:first'));
			imgs[this.data.id] = this.data.url; 
		}
		return this.data.url;
		});
		/* Once imgs object is prepared, continue */
		$.when.apply(null, deferreds.get()).then(function() { 

			hero.attr('src',imgs[$('article:first').find('img').attr('id')]).css('display','block');
			compute_images = function(imgs){
				var compute_image = function(v,k){
					var _width,_height,dfd = new $.Deferred();
					/* Create new offscreen image to test sizes, *Bonus, preload the images */
					$("<img/>").attr("src", v).load(function() {
						_width = this.width; 
						_height = this.height;
						imgAspect[k] = _width / _height;
						/*  We want to send images to get new thumbnail that is vertically locked */
						if(true|| (_width > _height || $('#'+k).attr('src') == 'default') && v.indexOf('.gif') == -1){
							squares[k] = v;
						}

						dfd.resolve(k);
					});
					return dfd.promise();
				}
			return $.map(imgs,compute_image);
			}
			
			promises = compute_images(imgs);
			/* Once the image sizes have been computed */
			$.when.apply(null, promises).then(function() {

				$.post('',squares, "json").done(function(response){
					$.each(response,function(idx, el){
						$('#'+idx).attr('src','/static/img/'+idx+'.jpg')
					});
				});
			}, function(e) {
				console.log("fail", this);    
			});
		});
	});


	/* Delegate some simple jQuery events */
	$('aside:first').delegate('input:first','click',function(event){
		var collage = {};
		$("#collage").remove();
		$('aside:first .imgs img').each(function(){
			collage[this.id] = imgs[this.id];
		});
            $('section#main .container:last').detach().appendTo('aside');
            $('section#main').html('').hide().css('background-color','#2B2B2B').fadeIn('slow');
            paper = Raphael($('#main').get(0),$('#main').width(),$('#main').height());
            var row = -1;
            var col = 0;
            var colHeight = {'-1':{}}
            $('aside:first .imgs img').each(function(idx,image){
                if(idx % 3 == 0){
                    row++;
                }
                if(!colHeight[row])
                    colHeight[row] = {};
                colHeight[row][idx%3] = 270 / imgAspect[$(image).attr('id')] ;
                var image = paper
                .image('/static/orig/'+$(image).attr('id') +'.jpg', (idx % 3) * 270, colHeight[row - 1][idx%3],  270, 270 / imgAspect[$(image).attr('id')]);

                image.click(function(){
                    this.toFront();
                    this.freeTransform.updateHandles();
                    $(fts).each(function(){this.hideHandles()});
                    this.freeTransform.showHandles();
                });	
                ft = paper.freeTransform(image);
                fts.push(ft);
                ft.setOpts({'attrs':{fill:'black','stroke':'white'},keepRatio:['axisX','axisY','bboxCorners','bboxSides']},function(){
                });
            });
            window.setTimeout(function(){
            fts[0].showHandles();
            },500);
            $('<button id="add_text">Add Text</button>').insertAfter('#main');
			return false;
	}).delegate('input:last','click',function(){
            $('#collage').remove();
            $(fts).each(function(){
                this.hideHandles();
            });
            var canvas = $('canvas')[0];
            var svg = paper.toSVG();
            canvg(canvas,svg , {
                renderCallback: function(){
                    $('div.spinner').css('background','url(static/img/ulogo.gif) top left no-repeat').html('Creating ');
                    $('aside a').remove();
                        var data = canvas.toDataURL('image/png',1)
                    $('#myModal p:first').html('<img src="' + data + '" />');
                    $('#myModal').reveal();
                    $.post('/collage', data, function(response){
                        $('div.spinner').hide();
                        $('<a id="collage" target="_blank" href="'+response+'">Download your collage</a>').insertAfter($('aside div.spinner,,reveal-modal h1:first'));
                    });
                }
            });
        });

   	$('.wrapper').delegate('img','hover click', function(event){
		if(event.type == 'mouseenter'){
			hero.attr('src',
			imgs[this.id]);
		}
		if(event.type == 'click'){
			if(!$(this).hasClass('selected')){
			$(this).addClass('selected');
			$(this).clone().appendTo('aside:first .imgs');
			} else {

			$(this).removeClass('selected');
			$('aside:first .imgs img#' + this.id).remove();
			}
		}
	}).delegate('button#add_text','click',function(){
            var text = prompt('Text to Add');
            var t =paper.text($('#main').width() / 2, $('#main').height() / 2,text);
            t.attr({ "font-size": '32px', 'fill':"#dfdfdf"});
            t.toFront()
            ft = paper.freeTransform(t);
        });
;
});



