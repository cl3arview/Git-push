 

(function($) {

	var $window = $(window),
		$body = $('body'),
		$wrapper = $('#wrapper'),
		$main = $('#main'),
		$panels = $main.children('.panel'),
		$nav = $('#nav'), $nav_links = $nav.children('a');

	// Breakpoints.
		breakpoints({
			xlarge:  [ '1281px',  '1680px' ],
			large:   [ '981px',   '1280px' ],
			medium:  [ '737px',   '980px'  ],
			small:   [ '361px',   '736px'  ],
			xsmall:  [ null,      '360px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Nav.
		$nav_links
			.on('click', function(event) {

				var href = $(this).attr('href');

				// Not a panel link? Bail.
					if (href.charAt(0) != '#'
					||	$panels.filter(href).length == 0)
						return;

				// Prevent default.
					event.preventDefault();
					event.stopPropagation();

				// Change panels.
					if (window.location.hash != href)
						window.location.hash = href;

			});

	// Panels.

		// Initialize.
			(function() {

				var $panel, $link;

				// Get panel, link.
					if (window.location.hash) {

				 		$panel = $panels.filter(window.location.hash);
						$link = $nav_links.filter('[href="' + window.location.hash + '"]');

					}

				// No panel/link? Default to first.
					if (!$panel
					||	$panel.length == 0) {

						$panel = $panels.first();
						$link = $nav_links.first();

					}

				// Deactivate all panels except this one.
					$panels.not($panel)
						.addClass('inactive')
						.hide();

				// Activate link.
					$link
						.addClass('active');

				// Reset scroll.
					$window.scrollTop(0);

			})();

		// Hashchange event.
			$window.on('hashchange', function(event) {

				var $panel, $link;

				// Get panel, link.
					if (window.location.hash) {

				 		$panel = $panels.filter(window.location.hash);
						$link = $nav_links.filter('[href="' + window.location.hash + '"]');

						// No target panel? Bail.
							if ($panel.length == 0)
								return;

					}

				// No panel/link? Default to first.
					else {

						$panel = $panels.first();
						$link = $nav_links.first();

					}

				// Deactivate all panels.
					$panels.addClass('inactive');

				// Deactivate all links.
					$nav_links.removeClass('active');

				// Activate target link.
					$link.addClass('active');

				// Set max/min height.
					$main
						.css('max-height', $main.height() + 'px')
						.css('min-height', $main.height() + 'px');

				// Delay.
					setTimeout(function() {

						// Hide all panels.
							$panels.hide();

						// Show target panel.
							$panel.show();

						// Set new max/min height.
							$main
								.css('max-height', $panel.outerHeight() + 'px')
								.css('min-height', $panel.outerHeight() + 'px');

						// Reset scroll.
							$window.scrollTop(0);

						// Delay.
							window.setTimeout(function() {

								// Activate target panel.
									$panel.removeClass('inactive');

								// Clear max/min height.
									$main
										.css('max-height', '')
										.css('min-height', '');

								// IE: Refresh.
									$window.triggerHandler('--refresh');

								// Unlock.
									locked = false;

							}, (breakpoints.active('small') ? 0 : 500));

					}, 250);

			});

	// IE: Fixes.
		if (browser.name == 'ie') {

			// Fix min-height/flexbox.
				$window.on('--refresh', function() {

					$wrapper.css('height', 'auto');

					window.setTimeout(function() {

						var h = $wrapper.height(),
							wh = $window.height();

						if (h < wh)
							$wrapper.css('height', '100vh');

					}, 0);

				});

				$window.on('resize load', function() {
					$window.triggerHandler('--refresh');
				});

			// Fix intro pic.
				$('.panel.intro').each(function() {

					var $pic = $(this).children('.pic'),
						$img = $pic.children('img');

					$pic
						.css('background-image', 'url(' + $img.attr('src') + ')')
						.css('background-size', 'cover')
						.css('background-position', 'center');

					$img
						.css('visibility', 'hidden');

				});

		}

})(jQuery);






function initComparisons() {
	var x, i;
	/* Find all elements with an "overlay" class: */
	x = document.getElementsByClassName("img-comp-overlay");
	for (i = 0; i < x.length; i++) {
	  /* Once for each "overlay" element:
	  pass the "overlay" element as a parameter when executing the compareImages function: */
	  compareImages(x[i]);
	}
	function compareImages(img) {
	  var slider, img, clicked = 0, w, h;
	  /* Get the width and height of the img element */
	  w = img.offsetWidth;
	  h = img.offsetHeight;
	  /* Set the width of the img element to 50%: */
	  img.style.width = (w / 2) + "px";
	  /* Create slider: */
	  slider = document.createElement("DIV");
	  slider.setAttribute("class", "img-comp-slider");
	  /* Insert slider */
	  img.parentElement.insertBefore(slider, img);
	  /* Position the slider in the middle: */
	  slider.style.top = (h / 2) - (slider.offsetHeight / 2) + "px";
	  slider.style.left = (w / 2) - (slider.offsetWidth / 2) + "px";
	  /* Execute a function when the mouse button is pressed: */
	  slider.addEventListener("mousedown", slideReady);
	  /* And another function when the mouse button is released: */
	  window.addEventListener("mouseup", slideFinish);
	  /* Or touched (for touch screens: */
	  slider.addEventListener("touchstart", slideReady);
	   /* And released (for touch screens: */
	  window.addEventListener("touchend", slideFinish);
	  function slideReady(e) {
		/* Prevent any other actions that may occur when moving over the image: */
		e.preventDefault();
		/* The slider is now clicked and ready to move: */
		clicked = 1;
		/* Execute a function when the slider is moved: */
		window.addEventListener("mousemove", slideMove);
		window.addEventListener("touchmove", slideMove);
	  }
	  function slideFinish() {
		/* The slider is no longer clicked: */
		clicked = 0;
	  }
	  function slideMove(e) {
		var pos;
		/* If the slider is no longer clicked, exit this function: */
		if (clicked == 0) return false;
		/* Get the cursor's x position: */
		pos = getCursorPos(e)
		/* Prevent the slider from being positioned outside the image: */
		if (pos < 0) pos = 0;
		if (pos > w) pos = w;
		/* Execute a function that will resize the overlay image according to the cursor: */
		slide(pos);
	  }
	  function getCursorPos(e) {
		var a, x = 0;
		e = (e.changedTouches) ? e.changedTouches[0] : e;
		/* Get the x positions of the image: */
		a = img.getBoundingClientRect();
		/* Calculate the cursor's x coordinate, relative to the image: */
		x = e.pageX - a.left;
		/* Consider any page scrolling: */
		x = x - window.pageXOffset;
		return x;
	  }
	  function slide(x) {
		/* Resize the image: */
		img.style.width = x + "px";
		/* Position the slider: */
		slider.style.left = img.offsetWidth - (slider.offsetWidth / 2) + "px";
	  }
	}
  }