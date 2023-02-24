<?php
// Connexion à la base de données
$connexion = mysqli_connect('localhost', 'utilisateur', 'password', 'site');

if (!$connexion) {
    die('La connexion à la base de données a échoué : ' . mysqli_connect_error());
}

// Récupération de l'ID de l'appareil depuis l'URL
$id_appareil = isset($_GET['id']) ? intval($_GET['id']) : 0;

// Récupération des informations de l'appareil depuis la base de données
$requete = "SELECT nom, version, statut, adresse_ip FROM appareils WHERE id = " . $id_appareil;
$resultat = mysqli_query($connexion, $requete);

if (!$resultat) {
    die('La requête SQL a échoué : ' . mysqli_error($connexion));
}

// Vérification si l'appareil existe
if (mysqli_num_rows($resultat) == 0) {
    die('L\'appareil demandé n\'existe pas.');
}

// Récupération des données de l'appareil
$appareil = mysqli_fetch_assoc($resultat);

// Fermeture de la connexion à la base de données
mysqli_close($connexion);
?>

<!-- Affichage des informations de l'appareil -->
<h1>Tableau de bord de l'appareil <?php echo $appareil['nom']; ?></h1>
<p>Version : <?php echo $appareil['version']; ?></p>
<p>Statut : <?php echo $appareil['statut']; ?></p>
<p>Adresse IP : <?php echo $appareil['adresse_ip']; ?></p>

<!-- Bouton pour redémarrer l'appareil -->
<form action="redemarrer_appareil.php" method="POST">
    <input type="hidden" name="id_appareil" value="<?php echo $id_appareil; ?>">
    <input type="submit" value="Redémarrer l'appareil">
</form>

<!DOCTYPE html>
<html>
<head>
	<title>Tableau de bord de l'appareil</title>
	<style>
		/* Style pour la mise en page */
		body {
			font-family: Arial, sans-serif;
			background-color: #F2F2F2;
			margin: 0;
			padding: 0;
		}
		.container {
			width: 80%;
			margin: 0 auto;
			background-color: #FFFFFF;
			padding: 20px;
			box-sizing: border-box;
			box-shadow: 0px 0px 10px #BBBBBB;
			border-radius: 5px;
			margin-top: 50px;
		}
		h1 {
			margin-top: 0;
		}
		table {
			border-collapse: collapse;
			width: 100%;
		}
		th, td {
			text-align: left;
			padding: 8px;
			border-bottom: 1px solid #ddd;
		}
		th {
			background-color: #333333;
			color: #FFFFFF;
		}
		.button {
			background-color: #4CAF50;
			border: none;
			color: white;
			padding: 8px 16px;
			text-align: center;
			text-decoration: none;
			display: inline-block;
			font-size: 14px;
			margin: 4px 2px;
			cursor: pointer;
			border-radius: 5px;
		}
		.button-reboot {
			background-color: #F44336;
		}
	</style>
</head>
<body>
	<div class="container">
		<h1>Tableau de bord de l'appareil</h1>
		<table>
			<thead>
				<tr>
					<th>Information</th>
					<th>Valeur</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>Nom de l'appareil</td>
					<td>SemaBox 1</td>
				</tr>
				<tr>
					<td>Version de l'appareil</td>
					<td>1.0</td>
				</tr>
				<tr>
					<td>Statut de l'appareil</td>
					<td><span style="color: green;">Connecté</span></td>
				</tr>
				<tr>
					<td>Adresse IP</td>
					<td>192.168.1.100</td>
				</tr>
			</tbody>
		</table>
		<p><a href="tableau_bord.php?id=1&cmd=reboot" class="button button-reboot">Redémarrer l'appareil</a></p>
	</div>
</body>
</html>
