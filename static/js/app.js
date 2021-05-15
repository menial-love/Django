var tips = function ($msg, $type, $icon, $from, $align) {
	$type  = $type || 'info';
	$from  = $from || 'top';
	$align = $align || 'center';
	$enter = $type == 'success' ? 'animated fadeInUp' : 'animated shake';

	jQuery.notify({
		icon: $icon,
		message: $msg
	},
	{
		element: 'body',
		type: $type,
		allow_dismiss: true,
		newest_on_top: true,
		showProgressbar: false,
		placement: {
			from: $from,
			align: $align
		},
		offset: 20,
		spacing: 10,
		z_index: 10800,
		delay: 3000,
		timer: 1000,
		animate: {
			enter: $enter,
			exit: 'animated fadeOutDown'
		}
	});
};

/**
 * 页面加载等待
 * @param $mode 'show', 'hide'
 * @author yinq
 */
var pageLoader = function ($mode) {
	var $loadingEl = jQuery('#loader-wrapper');
	$mode          = $mode || 'show';

	if ($mode === 'show') {
		if ($loadingEl.length) {
			$loadingEl.fadeIn(250);
		} else {
			jQuery('body').prepend('<div id="loader-wrapper"><div id="loader"></div></div>');
		}
	} else if ($mode === 'hide') {
		if ($loadingEl.length) {
			$loadingEl.fadeOut(250);
		}
	}

	return false;
};


$('a.like-review').click(function () {
    var $this = $(this);
    var rid = $this.data('rid');
    var action = $this.data('action');
    var ctg = $this.data('ctg');
    var likeCount = parseInt($this.find('span.like-count').text());
    var data = {
        'rid': rid,
        'action': action,
        'ctg': ctg
    };
    $.ajax({
        cache: false,
        type: 'POST',
        url: '/review/add/like/',
        data: data,
        async: true,
        success: function (response) {
            if (response.msg === 'ok'){
                $this.data('action', action === 'like' ? 'unlike' : 'like');
                if (action === 'like'){
                    $this.removeClass('text-muted');
                    $this.addClass('text-danger');
                    $this.find('span.like-thumbs').html('<i class="fa fa-thumbs-up" aria-hidden="true"></i>');
                    $this.find('span.like-count').text(likeCount + 1);
                    tips('+1', 'success');
                } else {
                    $this.removeClass('text-danger');
                    $this.addClass('text-muted');
                    $this.find('span.like-thumbs').html('<i class="fa fa-thumbs-o-up" aria-hidden="true"></i>');
                    $this.find('span.like-count').text(likeCount - 1);
                }

            }
        }
    });
});


$('a.sticky-post').click(function () {
    var $this = $(this);
    var rid = $this.data('pid');
    var action = $this.data('action');
    var data = {
        'pid': rid,
        'action': action
    };
    $.ajax({
        cache: false,
        type: 'POST',
        url: '/post/sticky/',
        data: data,
        async: true,
        success: function (response) {
            if (response.msg === 'ok'){
                $this.data('action', action === 'sticky' ? 'unsticky' : 'sticky');
                if (action === 'sticky'){
                    $this.removeClass('text-muted');
                    $this.addClass('text-red');
                    $this.text('已顶置');
                    tips('已顶置', 'success');
                } else {
                    $this.removeClass('text-red');
                    $this.addClass('text-muted');
                    $this.text('顶置');
                }

            }
        }
    });
});