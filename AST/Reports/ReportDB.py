from AST.Expressions.Literal import TYPE_DECLARATION
from AST.Expressions.AccessInstruction import AccessInstruction
from AST.Expressions.AccessTypeArray import AccessTypeArray
from AST.Expressions.AccessTypeVector import AccessTypeVector
from AST.Instructions.Modulo import Modulo
class ReportDB:
    def __init__(self, modules):      
        self.modules = modules
        html = open("ReportDB.html", "w")
        html.write("""<!DOCTYPE html>
            <html lang="en">

            <head>

                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <meta name="description" content="">
                <meta name="author" content="TemplateMo">
                <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700" rel="stylesheet">

                <title>Reporte</title>

                <!-- Bootstrap core CSS -->
                <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

                <!-- Additional CSS Files -->
                <link rel="stylesheet" href="assets/css/fontawesome.css">
                <link rel="stylesheet" href="assets/css/templatemo-host-cloud.css">
                <link rel="stylesheet" href="assets/css/owl.css">
            <!--

            Host Cloud Template

            https://templatemo.com/tm-541-host-cloud

            -->
            </head>

            <body>
        <!-- Header -->
        <header class="">
        <nav class="navbar navbar-expand-lg">
            <div class="container">
            <a class="navbar-brand" href="ReportSymbol.html"><h2>Reportes<em>OLC2</em></h2></a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ml-auto">
                </ul>
            </div>
            <div class="functional-buttons">
            </div>
            </div>
        </nav>
        </header>

        <!-- Page Content -->
        <!-- Banner Starts Here -->
        <div class="banner">
        <div class="container">
            <div class="row">
            <div class="col-md-8 offset-md-2">
                <div class="header-text caption">
                <h2 style=>Reporte de</h2>
                <h1 style="color: white; font-size:120px; text-align: center; font-style: italic; font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif; text-transform:uppercase">DB</h1>
                </div>
            </div>
            </div>
        </div>
        </div>
        <!-- Banner Ends Here -->
        """)
        html.write("""<!-- Ascendente Starts Here -->
            <div style="padding-bottom: 100px;" class="services-section">
                <div class="container">
                    <div class="row">
                        <div class="col-md-8 offset-md-2">
                            <div class="section-heading">
                            <h2 style="text-transform:uppercase; text-align: center;">Tablas de bases de datos</h2>
                            </div>
                            <table class="table">
                            <thead style="color:white; background-color: rgb(0, 50, 199); text-transform:uppercase; text-align: center;">
                                <tr>
                                <th scope="col">No.</th>
                                <th scope="col">Nombre tabla</th>
                                <th scope="col">Nombre DB</th>
                                <th scope="col">Fila</th>
                                <th scope="col">Columna</th>
                                </tr>
                            </thead>
                            <tbody>
                            """)
        count = 1
        for module in self.modules:
            id = module.id
            for table in module.instructions.instructions:
                if isinstance(table.instruction,Modulo):
                    html.write("""<tr>
                    <td style="text-align: center;">""" + str(count) + """</td>
                    <td style="text-align: center;">""" + str(table.instruction.id) + """</td>
                    <td style="text-align: center;">""" + str(id) + """</td>
                    <td style="text-align: center;">""" + str(table.instruction.row) + """</td>
                    <td style="text-align: center;">""" + str(table.instruction.column) + """</td>
                    </tr>""")
                    count += 1

        html.write("""
                    </tbody>
                        </table>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
                <!-- Services Ends Here -->""")
        
        print("\n")
        print("Reporte creado con exito")
        print("\n")

        html.write("""<!-- Bootstrap core JavaScript -->
                <script src="vendor/jquery/jquery.min.js"></script>
                <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

                <!-- Additional Scripts -->
                <script src="assets/js/custom.js"></script>
                <script src="assets/js/owl.js"></script>
                <script src="assets/js/accordions.js"></script>


                <script language = "text/Javascript"> 
                cleared[0] = cleared[1] = cleared[2] = 0; //set a cleared flag for each field
                function clearField(t){                   //declaring the array outside of the
                if(! cleared[t.id]){                      // function makes it static and global
                    cleared[t.id] = 1;  // you could use true and false, but that's more typing
                    t.value='';         // with more chance of typos
                    t.style.color='#fff';
                    }
                }
                </script>
            </body>
            </html>
        """)
        html.close()