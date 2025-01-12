$(function() {
    let item = ""

    $(".Task_List").on("click", "div", function() {
        $("#selected").removeAttr("id")
        $(this).attr("id", "selected")
    })

    $(".Buttons").on("click", "#delete", function() {
        item = $("#selected li").text()
        fetch("/delete", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ item: item }),
        })
        .then(response => {
            if (response.redirected) {
            // Redirect to the home page if the server indicates a redirect
            window.location.href = response.url;
            }
            else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.message) {
                console.log(data.message); // Success message
            }
            else if (data && data.error) {
                console.error(data.error); // Error message
            }
        })
        .catch(error => console.error('Error:', error));
    })

    $(".Buttons").on("click", "#edit", function() {
        item = $("#selected li").text()
        fetch("/edit_js", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ item: item })
        })
        .then(response => response.text())
        .then(html => {
            $(".center-wrapper").html(html)
        })
        .catch(error => console.log("Error", error))
    });

    $(".center-wrapper").on("submit", "#editForm", function (event) {
        event.preventDefault();  // Prevent the default form submission

        const task = $("#taskInput").val();  // Get the new task value from the input field

        fetch("/edit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ item: item, task: task })  // Send both the original item and the updated task
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;  // Redirect to the home page
            } else if (data.error) {
                console.error(data.error);  // Handle any errors
            }
        })
        .catch(error => console.error('Error:', error));
    });


    $(".center-wrapper").on("keydown keyup", ".form-control", function(e) {
        if (e.key == "Enter") {
            $(".btn btn-primary").click()
        }
    })
})