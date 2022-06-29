$(function(){
    
    var toaster = `
    <div id="showToast" class="toast w-100 align-items-center" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="d-flex w-100">
    <div class="toast-body">
    <p id="messages"><h1>Supppppp</h1></p>
    </div>
    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    </div>
    `
    // $('#showToast').html(toaster)
    // console.log($('#showToast').html())
    $('#showToast').toast('show');
    $('#showToast').toast({autohide: false});
    const fixturesList = document.querySelector('#fixtures-list')
    const tidForm = document.querySelector('#tokenForm')


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
                // $('#showToast #messages').empty();
                // $('#showToast #messages').html('YourTransaction id was added successfully');
                $('#showToast').toast('show');
                $('#showToast').toast({autohide: false});
                console.log($('#showToast'))
            },
            error: function(err){
                console.log(err)
            }
        });

    })




    setInterval(function(){

        $.ajax({
            type: 'GET',
            url: fixturesList.dataset.url,
            success: function(response){
                // console.log(response)
                $('#fixtures-list').empty()
                // var url = response.fixtures[fixture].fixture_id
                for(var fixture in response.fixtures){
                    var fx = `<li class="list-group-item text-center lead py-4">
                        <div class="row">
                            <div class="col-9">
                                <img src="${response.fixtures[fixture].home_logo}" alt="club-logo"> <b> ${response.fixtures[fixture].home_name} </b> ${response.fixtures[fixture].home_goals} <b>vs</b> ${response.fixtures[fixture].away_goals} <b> ${response.fixtures[fixture].away_name} </b>  <img src="${response.fixtures[fixture].away_logo}" alt="club-logo">
                            </div>
                            <div class="col-3">
                                <a class="btn btn-sm btn-primary ms-auto" href="${response.fixtures[fixture].link}">Predict</a>
                            </div>
                        </div>
                    </li>`
                    $('#fixtures-list').append(fx);
                }
            },
            error:function(err){
                console.log('err')
            }
        });
    }, 500000);


})
