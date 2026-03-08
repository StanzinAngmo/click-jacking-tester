from urllib.request import urlopen
from sys import argv, exit
import webbrowser

def check(url):
    try:
        if "http" not in url:
            url = "http://" + url

        data = urlopen(url)
        headers = data.info()

        if "X-Frame-Options" not in headers:
            return True
        else:
            return False

    except:
        return None


def generate_report(results):

    html = """
    <html>
    <head>
    <title>Clickjacking Security Report</title>
    <style>
    body{
        font-family: Arial;
        margin:40px;
        background:#f5f5f5;
    }

    h1{
        color:#333;
    }

    .safe{
        color:green;
        font-weight:bold;
    }

    .vulnerable{
        color:red;
        font-weight:bold;
    }

    .box{
        background:white;
        padding:20px;
        margin:15px 0;
        border-radius:8px;
        box-shadow:0px 2px 5px rgba(0,0,0,0.2);
    }
    </style>
    </head>

    <body>

    <h1>Website Clickjacking Security Report</h1>

    <p>This report checks whether websites are protected against
    <b>Clickjacking attacks</b>.</p>

    <p>Clickjacking happens when attackers load a website inside an invisible
    frame and trick users into clicking something malicious.</p>

    <h2>Scan Results</h2>
    """

    for site, status in results.items():

        if status == True:
            html += f"""
            <div class="box">
            <h3>{site}</h3>
            <p class="vulnerable">⚠ Vulnerable to Clickjacking</p>
            <p>This website does not use the <b>X-Frame-Options</b> security header,
            meaning it could potentially be embedded inside malicious pages.</p>
            </div>
            """

        elif status == False:
            html += f"""
            <div class="box">
            <h3>{site}</h3>
            <p class="safe">✔ Protected</p>
            <p>This website uses security headers that help prevent clickjacking attacks.</p>
            </div>
            """

        else:
            html += f"""
            <div class="box">
            <h3>{site}</h3>
            <p>Could not analyze this website.</p>
            </div>
            """

    html += """
    </body>
    </html>
    """

    with open("clickjacking_report.html", "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open("clickjacking_report.html")


def main():

    try:
        sites = open(argv[1]).read().splitlines()
    except:
        print("Usage: python clickjack_report.py sites.txt")
        exit()

    results = {}

    for site in sites:
        print("Checking:", site)
        results[site] = check(site)

    generate_report(results)


if __name__ == "__main__":
    main()