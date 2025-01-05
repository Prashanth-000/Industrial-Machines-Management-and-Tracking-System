pip install weasyprint
pip install pdfkit
Go to the wkhtmltopdf downloads page.
Download the Windows installer (choose the latest stable version).
Install the downloaded .exe file.
then change path as below---line 645(inside download_report route) for
path_to_wkhtmltopdf = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

Now Run app.py

 <!-- Flash Messages -->

        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul class="flashes">
                {% for category, message in messages %}
                    <li class="alert alert-{{ category }}">{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
        {% endwith %}

 <script>
        // Automatically hide flash messages after 3 seconds
        window.onload = function() {
            setTimeout(function() {
                const flashMessages = document.querySelectorAll('.flashes li');
                flashMessages.forEach(message => {
                    message.style.transition = "opacity 0.5s ease-out";
                    message.style.opacity = 0;
                    setTimeout(() => message.remove(), 500);
                });
            }, 3000);
        };
    </script>

        .flashes {
            list-style-type: none;
            padding: 0;
            margin-bottom: 20px;
        }
        .flashes li {

            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .alert-success {
            background-color: #76f0a9;
            color: white;
            color: rgb(0, 0, 0);
        }
        .alert-error {
            background-color: #e74c3c;
            color: white;
        }
        .alert-info {
            background-color: #189599; /* Light blue for logout message */
            color: white;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
