<!DOCTYPE html>
<html>
<head>
	<title>Mon site web</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="style.css">
</head>
<body>
	<header>
		<h1>Liste d'appareils connectés</h1>
	</header>
	<main>
		<section class="appareils">
			<h2>Liste d'appareils</h2>
				<?php
				// Connexion à la base de données
				$host = 'localhost';
				$dbname = 'site';
				$username = 'utilisateur';
				$password = 'password';

				try {
					$bdd = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
				} catch (PDOException $e) {
					die("Erreur : " . $e->getMessage());
				}
				// Récupération des appareils depuis la base de données
				$req = $bdd->query("SELECT * FROM appareils");
				$appareils = $req->fetchAll(PDO::FETCH_ASSOC);
				?>
				<!-- Affichage de la liste des appareils -->
				<ul>
				  <?php foreach ($appareils as $appareil) : ?>
					<li>
					  <a href="tableau_bord.php?id=<?php echo $appareil['id']; ?>">
						<?php echo $appareil['nom']; ?>
					  </a>
					</li>
				  <?php endforeach; ?>
				</ul>
		</section>
	</main>
	<footer>
		<p>Mon site web © 2023</p>
	</footer>
</body>
</html>
