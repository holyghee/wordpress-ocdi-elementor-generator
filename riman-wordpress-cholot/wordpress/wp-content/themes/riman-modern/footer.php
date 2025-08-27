<footer class="site-footer">
    <div class="footer-content">
        <div class="footer-grid">
            <div class="footer-column">
                <h3>RIMAN GmbH</h3>
                <p>Ihr Partner für professionelles Rückbaumanagement, Altlastensanierung und Mediation.</p>
            </div>
            
            <div class="footer-column">
                <h4>Dienstleistungen</h4>
                <ul>
                    <li><a href="<?php echo esc_url(home_url('/rueckbaumanagement')); ?>">Rückbaumanagement</a></li>
                    <li><a href="<?php echo esc_url(home_url('/altlastensanierung')); ?>">Altlastensanierung</a></li>
                    <li><a href="<?php echo esc_url(home_url('/mediation')); ?>">Mediation</a></li>
                    <li><a href="<?php echo esc_url(home_url('/schadstoff-management')); ?>">Schadstoffmanagement</a></li>
                </ul>
            </div>
            
            <div class="footer-column">
                <h4>Schnellzugriff</h4>
                <ul>
                    <li><a href="<?php echo esc_url(home_url('/ueber-uns')); ?>">Über uns</a></li>
                    <li><a href="<?php echo esc_url(home_url('/referenzen')); ?>">Referenzen</a></li>
                    <li><a href="<?php echo esc_url(home_url('/infothek')); ?>">Infothek</a></li>
                    <li><a href="<?php echo esc_url(home_url('/mitgliederbereich')); ?>">Mitgliederbereich</a></li>
                </ul>
            </div>
            
            <div class="footer-column">
                <h4>Kontakt</h4>
                <div class="footer-contact">
                    <p>Musterstraße 123<br>12345 Musterstadt</p>
                    <p>Tel: <a href="tel:+49123456789">+49 (0) 123 456789</a></p>
                    <p>Email: <a href="mailto:info@riman.de">info@riman.de</a></p>
                </div>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>© <?php echo date('Y'); ?> RIMAN GmbH. Alle Rechte vorbehalten. | 
                <a href="<?php echo esc_url(home_url('/impressum')); ?>">Impressum</a> | 
                <a href="<?php echo esc_url(home_url('/datenschutz')); ?>">Datenschutz</a> | 
                <a href="<?php echo esc_url(home_url('/agb')); ?>">AGB</a>
            </p>
        </div>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>