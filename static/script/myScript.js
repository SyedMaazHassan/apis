/* JS comes here */
var qr;
var firstname = "";
(function() {
        qr = new QRious({
        element: document.getElementById('employee-qr'),
        size: 150,
        // value: 'https://studytonight.com'
    });
})();

function generateQRCode(myqrtext) {
    var qrtext = myqrtext;
    // document.getElementById("qr-result").innerHTML = "QR code for " + qrtext +":";
    // alert(qrtext);
    qr.set({
        foreground: 'black',
        size: 200,
        value: qrtext
    });
}

function print_card() {
    let new_card = new jsPDF();
    let my_card_section = document.getElementById("myIdCard");
    new_card.fromHTML(my_card_section, 15, 15);
    new_card.save(`${firstname}-id-card.pdf`);
    // document.getElementById('myIdCard').contentWindow.print();
}

function format_time(timeString) {
    const timeString12hr = new Date('1970-01-01T' + timeString + 'Z')
        .toLocaleTimeString({},
            {timeZone:'UTC',hour12:true,hour:'numeric',minute:'numeric'}
        );
    return timeString12hr;
}

$(".view-my-card").on("click", function () {
    let myID = $(this).prop("id");
    $.ajax({
        url: "/getEmployee",
        type: "GET",
        data: {
            employee_id: myID
        },
        success: (response)=>{
            if (response.status) {
                firstname = response.employee_info.first_name;
                $("#employee-name").html(`<h3 class="my-0 mb-2">${response.employee_info.first_name}</h3><h4 class="my-0">${response.employee_info.last_name}</h4>`);
                generateQRCode(response.employee_info.unique_id);

                let days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
                let myDivFrom = `<tr>`;
                let myDivTo = `<tr>`;
                let myDivMiddle = "<tr>";
                

                
                for (let i = 0; i < days.length; i++) {
                    const day = days[i];

                    myDivFrom += `
                        <td>${format_time(response.employee_info.timings[day]["start"])}</td>
                    `;

                    myDivTo += `
                        <td>${format_time(response.employee_info.timings[day]["end"])}</td>
                    `;

                    myDivMiddle += "<td><b>to</b></td>";
                    
                }

                myDivFrom += "</tr>";
                myDivTo += "</tr>";
                myDivMiddle += `</tr>`;

                $("#myBody").html(
                    myDivFrom + myDivMiddle + myDivTo
                )
                
                
                $("#myCard").modal("show");
            }
        }
    });
});

document.getElementById("download-btn").addEventListener("click", ()=>{
    const my_id_card = document.getElementById("myIdCard");
    let option = {
        'margin': [20, 35],
        'filename': firstname+"-id-card"
    }
    html2pdf().from(my_id_card).set(option).save();
});
