$(function(){
    
    $('#showToast').toast('show');
    $('#showToast').toast({autohide: false});
    const fixturesList = document.querySelector('#fixtures-list')
    const tidForm = document.querySelector('#tokenForm')

    
    

    // SUBMIT TOKENS AUTOMATICALLY
    $('#tokenForm').submit(function(e){
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: tidForm.dataset.url,
            data: {
                t_id: $('#id_t_id').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response){
                var message = response.result
                var toastBody = `
                <div id='toasty'  class="toast w-100 align-items-center mx-auto bg-white" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex w-100">
                    <div class="toast-body">
                    <p id="tmessages">${message}</p>
                    </div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                </div>
                `
                $('#id_t_id').val('')
                $('#toaster').html(toastBody);
                $('#toasty').toast('show');
                $('#toasty').toast({autohide: false});
            },
            error: function(err){
                console.log(err)
            }
        });

    })



    // A WAY TO MAKE PREDICTIONS AJAXLY BUT FORMS WOULD HAVE TO BE IN PAGE ALREADY
    // SOLVED MOTHERFUCKER
    $('#fixtures-list').find('a').click(function(e){
        e.preventDefault()
        fixtureUrl = $(this).attr('href')

        $.ajax({
            type: 'GET',
            url: fixtureUrl,
            success: function(prediction){
                for(var fixture in prediction.fixture){
                    var p = prediction.fixture[fixture]

                    var predictionForm = `
                    <span>
                        <b>Home: </b>
                        <img src="${p.home_logo}" alt="club-logo">
                    </span>
                    
                    <input type="text" id="home_logo" name="home_logo" value="${p.home_logo}" hidden>


                    <span>${p.home_name}</span>
                    <input type="text" id="home_name" name="home_name" value="${p.home_name}" hidden>

                    <br><br>

                    Home goals:
                    <input type="text" name="home_goals" maxlength="2" required id="id_home_goals">
                    
                    <br><br><hr><br>

                    <span>
                        <b>Away: </b>
                        <img src="${p.away_logo}" alt="club-logo">
                    </span>
                    
                    <input type="text" id="away_logo" name="away_logo" value="${p.away_logo}" hidden>
                    <input type="text" name="link" id="predictLink" data-link="${p.link}" value="${p.link}" hidden>

                    <span>${p.away_name}</span>
                    
                    <input type="text" id="away_name" name="away_name" value="${p.away_name}" hidden="">

                    <br><br>

                    Away goals: 
                    <input type="text" name="away_goals" maxlength="2" required="" id="id_away_goals">
                    
                    <hr>
                    <br>
                    `
                    $('#predictForm #formElems').empty()
                    $('#predictForm #formElems').append(predictionForm)
                }
            },
            error: function(err){
                console.log('err', err)
            }
        })
    })



    // AJAX TESTER
    // $('#getpres').click(function(){
    //     get_predictions()
    // })




    // REFRESHES PREDICTIONS AFTER
    function get_predictions(){
        const mypTable = document.querySelector('#predictGet')
        
        $.ajax({
            type: 'GET',
            url: mypTable.dataset.mypredict,
            dataType: 'json',
            success: function(answers){
                
                var count = 1
                $('#myTable').empty()
                var myTable

                for (var pre in answers.predictions){
                    console.log(answers.predictions[pre])
                    var p = answers.predictions[pre]
                    myTable = `
                    <tr>
                        <th scope="row" class="py-3">${count}</th>
                        <td class="py-3">
                        <img src="${p.home_logo}" alt="club-logo">
  
                        <b>${p.home_name}</b>
                        
                        ${p.home_goals} 
    
                        <b>vs</b>
                        
                        ${p.away_goals}
    
                        <b>${p.away_name }</b> 
    
                        <img src="${p.away_logo }" alt="club-logo">
                        </td>
                        <td class="py-3">${p.points }</td>
                    </tr>
                    `

                    count += 1
                    $('#myTable').append(myTable)
                }
                
            },
            error:function(err){
                console.log('err')
            }
        });
    }





    // SUBMITS PREDICTION FORM AND SHOWS TOAST
    $('#predictForm').submit(function(e){
        e.preventDefault()
        const predictLink = document.querySelector('#predictLink')


        $.ajax({
            type: 'POST',
            url: predictLink.dataset.link,
            data: {
                home_name: $('#home_name').val(),
                home_logo: $('#home_logo').val(),
                away_name: $('#away_name').val(),
                away_logo: $('#away_logo').val(),
                home_goals: $('#id_home_goals').val(),
                away_goals: $('#id_away_goals').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(receive){
                message = receive.result
                var toastBody = `
                <div id='toasty'  class="toast w-100 align-items-center mx-auto bg-white" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex w-100">
                    <div class="toast-body">
                    <p id="tmessages">${message}</p>
                    </div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                </div>
                `

                $('#closePredict').click()
                $('#predictForm #formElems').empty()
                $('#toaster').html(toastBody);
                $('#toasty').toast('show');
                $('#toasty').toast({autohide: false});
                get_predictions()
            },
            error: function(err){
                console.log(err)
            }
        })


    })






    function scoresGetter(){
        $.ajax({
            type: 'GET',
            url: fixturesList.dataset.url,
            success: function(response){
                console.log('response' ,response)
                $('#fixtures-list').each(function(){

                    $(this).find('span').each(function(){

                        console.log($(this).html())

                        for(var fixture in response.fixtures){

                        if ($(this).attr('id') == response.fixtures[fixture].fixture_id){
                            $(this).empty();
                            var scores = `${response.fixtures[fixture].home_goals} <b>vs</b> ${response.fixtures[fixture].away_goals}`
                            $(this).append(scores);
                        }}
                    })
                })


            },
            error:function(err){
                console.log('err')
            }
        });
    }



    // UPDATES SCORES EVERY 5 SECONDS
     setInterval(function(){
           scoresGetter(), 5000});


    
    // AJAX TESTER
    $('#getpres').click(function(){
        alert(fixturesList, fixturesList.dataset.url, 'fixtures');
        scoresGetter();
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    // SUPPOSED TO START API CALLS AJAXLY BUT MEH
    // $('#adminForm').submit(function(e){
    //     var apiCalls = document.querySelector('#adminForm')
    //     e.preventDefault()
    
    //     console.log($('#until').val())
    //     $.ajax({
    //         type: 'POST',
    //         url: apiCalls.dataset.admin,
    //         data: {
    //             until: $('#until').val(),
    //             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    //         },
    //         success: function(response){
    //             msg = response.result
    //                 var toastBody = `
    //                 <div id='toasty'  class="toast w-100 align-items-center mx-auto" role="alert" aria-live="assertive" aria-atomic="true">
    //                 <div class="d-flex w-100">
    //                     <div class="toast-body">
    //                     <p id="tmessages">${msg}</p>
    //                     </div>
    //                     <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    //                 </div>
    //                 </div>
    //                 `
    
    //                 $('#until').empty()
    //                 $('#toaster').html(toastBody);
    //                 $('#toasty').toast('show');
    //                 $('#toasty').toast({autohide: false});
    //         },
    //         error: function(err){
    //             console.log(err);
    //                 var toastBody = `
    //                 <div id='toasty'  class="toast w-100 align-items-center mx-auto" role="alert" aria-live="assertive" aria-atomic="true">
    //                 <div class="d-flex w-100">
    //                     <div class="toast-body">
    //                     <p id="tmessages">Something went wrong</p>
    //                     </div>
    //                     <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    //                 </div>
    //                 </div>
    //                 `
    
    //                 $('#toaster').html(toastBody);
    //                 $('#toasty').toast('show');
    //                 $('#toasty').toast({autohide: false});
    //         }
    //     })
    // })





// TEMPLATE SCRIPTS

//  Count Up
function counter() {
    var oTop;
    if ($('.counter').length !== 0) {
      oTop = $('.counter').offset().top - window.innerHeight;
    }
    if ($(window).scrollTop() > oTop) {
      $('.counter').each(function () {
        var $this = $(this),
          countTo = $this.attr('data-count');
        $({
          countNum: $this.text()
        }).animate({
          countNum: countTo
        }, {
          duration: 1000,
          easing: 'swing',
          step: function () {
            $this.text(Math.floor(this.countNum));
          },
          complete: function () {
            $this.text(this.countNum);
          }
        });
      });
    }
  }
$(window).on('scroll', function () {
    counter();
		//.Scroll to top show/hide
    var scrollToTop = $('.scroll-top-to'),
      scroll = $(window).scrollTop();
    if (scroll >= 200) {
      scrollToTop.fadeIn(200);
    } else {
      scrollToTop.fadeOut(100);
    }
  });
	// scroll-to-top
  $('.scroll-top-to').on('click', function () {
    $('body,html').animate({
      scrollTop: 0
    }, 500);
    return false;
  });






  $('.usersPreds').click(function(e){
    e.preventDefault()
    var userPredTable = $(this).attr('href')

    $.ajax({
        type: 'GET',
        url: userPredTable,
        success: function(prediction){
            console.log(prediction)
            count = 1
            $('#predTable').empty()
            for(var fixture in prediction.predictions){
                var p = prediction.predictions[fixture]

                var predictionForm = `
                                    <tr>
                                        <th scope="row" class="py-3">${count}</th>
                                        <td class="py-3">
                                            <img src="${ p.home_logo }" alt="club-logo"> 
                                            <b>${ p.home_name}</b> 
                                        </td>
                                        <td class="py-3 goals">
                                            <span id="${ p.fixture_id }">  ${ p.home_goals} <b>vs</b> ${ p.away_goals} </span>
                                        </td>
                                        <td class="py-3">
                                            <b>${ p.away_name }</b>  
                                            <img src="${ p.away_logo }" alt="club-logo">
                                        </td>
                                        <td class="py-3">${ p.points }</td>
                                        <td class="py-3">${ p.date_created }</td>
                                    </tr>
                `
                // console.log('predictionForm', predictionForm)
                $('#predTable').append(predictionForm)
                count+=1
            }
        },
        error: function(err){
            console.log('err', err)
        }
    })
})













})







