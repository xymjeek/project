document.addEventListener('DOMContentLoaded', function() {
			var slider_content = document.querySelector('#banner .slider_list');
			var slider_items = slider_content.children;
			var num = slider_items.length;
			slider_content.style.width = (num + 2) * 100 + '%';
			slider_content.style.transform = 'translateX(-' + 100 / (num + 2) + '%)';
			slider_content.appendChild(slider_items[0].cloneNode(true));
			slider_content.insertBefore(slider_items[num - 1].cloneNode(true), slider_items[0]);
			var pagination = document.querySelector('#banner ol');
			for(var i = 0; i < num; i++) {
				var creatLi = document.createElement('li');
				pagination.appendChild(creatLi);
			}
			for(var i = 0; i < num + 2; i++) {
				slider_items[i].style.width = 100 / (num + 2) + '%';
			}
			var pagination_items = pagination.children;
			pagination_items[0].classList.add('active');
			var iNow = 1;
			var x = -iNow * slider_items[0].offsetWidth;
			//在这里设置一个开关,是css运动结束后解锁
			var bReady = true;
			slider_content.addEventListener('touchstart', function(ev) {
				//clearInterval(timer);//当滑屏的时候,是否要停止自动轮播
				if(bReady == false) {
					return;
				}
				bReady = false;
				slider_content.style.transition = 'none';
				var disX = ev.targetTouches[0].pageX - x;
				var downX = ev.targetTouches[0].pageX;

				function fnMove(ev) {
					x = ev.targetTouches[0].pageX - disX ;
					slider_content.style.transform = 'translate3d(' + x + 'px,0,0)';
				}

				function fnEnd(ev) {
					var upX = ev.changedTouches[0].pageX;
					//判断是否移动距离大于50
					if(Math.abs(upX - downX) > 50) {
						//左边移动
						if(upX - downX < 0) {
							iNow++;
							if(iNow == slider_items.length) {
								iNow = slider_items.length ;
							}
							if(iNow == num + 1) {
								pagination_items[num - 1].classList.remove('active');
								pagination_items[0].classList.add('active');
							} else {
								pagination_items[iNow - 1].previousElementSibling.classList.remove('active');
								pagination_items[iNow - 1].classList.add('active');
							}

						} else {
							//右边移动
							iNow--;
							if(iNow == -1) {
								iNow = 0;
							}
							if(iNow == 0) {
								pagination_items[0].classList.remove('active');
								pagination_items[num - 1].classList.add('active');
							} else {
								pagination_items[iNow - 1].nextElementSibling.classList.remove('active');
								pagination_items[iNow - 1].classList.add('active');
							}
						}
					}
					//储存此时ul的位置
					x = -iNow * slider_items[0].offsetWidth ;
					slider_content.style.transform = 'translate3d(' + x + 'px,0,0)';
					slider_content.style.transition = '500ms all ease';

					//监听li 当移动到两端的li时  瞬间移回
					function tEnd() {
						if(iNow == num + 1) {
							iNow = 1;
						}
						if(iNow == 0) {
							iNow = num;
						}
						slider_content.style.transition = 'none'
						x = -iNow * slider_items[0].offsetWidth ;
						slider_content.style.transform = 'translate3d(' + x + 'px,0,0)';
						bReady = true;
					}
					slider_content.addEventListener('transitionend', tEnd, false);
					//释放内存
					document.removeEventListener('touchend', fnEnd, false);
					document.removeEventListener('touchmove', fnMove, false);
				}

				document.addEventListener('touchmove', fnMove, false);
				document.addEventListener('touchend', fnEnd, false);
				//阻止默认事件
				ev.preventDefault();
			}, false);

			//自动轮播
			var timer=setInterval(function() {
				iNow++;
				if(iNow == num + 1) {
					x = -1 * slider_items[0].offsetWidth ;
					pagination_items[num - 1].classList.remove('active');
					pagination_items[0].classList.add('active');
					slider_content.style.transition = 'none';
					slider_content.style.transform = 'translate3d(' + 0 * slider_items[0].offsetWidth + 'px,0,0)';
					setTimeout(function() {
						slider_content.style.transition = '500ms all ease';
						slider_content.style.transform = 'translate3d(' + x + 'px,0,0)';
					})
					bReady = true;
					iNow = 1;
				} else {
					slider_content.style.transition = 'none';
					x = -iNow * slider_items[0].offsetWidth ;
					slider_content.style.transform = 'translate3d(' + x + 'px,0,0)';
					slider_content.style.transition = '500ms all ease';
					bReady = true;
					pagination_items[iNow - 1].previousElementSibling.classList.remove('active');
					pagination_items[iNow - 1].classList.add('active');
				}
			}, 5000);
		}, false);