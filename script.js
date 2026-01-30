// Only runs if #three-container exists (i.e., on home page)
const container = document.getElementById('three-container');
if (container) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    const ambient = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambient);
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(5, 10, 7.5);
    scene.add(dirLight);

    // Simple fallback rotating sphere (Earth-like) if no models loaded
    const geometry = new THREE.SphereGeometry(4, 32, 32);
    const material = new THREE.MeshStandardMaterial({
        color: 0x2e7d32,
        metalness: 0.1,
        roughness: 0.8
    });
    const globe = new THREE.Mesh(geometry, material);
    scene.add(globe);

    camera.position.set(0, 0, 12);
    controls.update();

    function animate() {
        requestAnimationFrame(animate);
        globe.rotation.y += 0.003;
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}