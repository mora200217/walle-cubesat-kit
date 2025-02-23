import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import Stats from "three/examples/jsm/libs/stats.module";

export const Viz = () => {
    const mountRef = useRef(null);

    useEffect(() => {
        const scene = new THREE.Scene();
        scene.add(new THREE.AxesHelper(5));

        const light = new THREE.SpotLight();
        light.position.set(20, 20, 20);
        scene.add(light);

        const camera = new THREE.PerspectiveCamera(
            75,
            mountRef.current.clientWidth / mountRef.current.clientHeight,
            0.1,
            1000
        );
        camera.position.z = 3;

        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
        mountRef.current.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        const loader = new STLLoader();
        loader.load(
            "/example.stl", // Asegúrate de que este archivo esté en la carpeta "public/"
            function (geometry) {
                const material = new THREE.MeshStandardMaterial({ color: 0x00ff00, wireframe: true  });
                const mesh = new THREE.Mesh(geometry, material);
                scene.add(mesh);
                
            },
            (xhr) => console.log((xhr.loaded / xhr.total) * 100 + "% loaded"),
            (error) => console.error("Error loading STL:", error)
        );

        window.addEventListener("resize", onWindowResize);
        function onWindowResize() {
            camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
        }

        const stats = new Stats();
        mountRef.current.appendChild(stats.dom);

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
            stats.update();
        }

        animate();

        return () => {
            window.removeEventListener("resize", onWindowResize);
            mountRef.current.removeChild(renderer.domElement);
        };
    }, []);

    return (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            {/* <img src="http://192.168.223.236:5000/video_feed" alt="Stream" style={{ width: "300px", margin:" 20px",  position: "fixed", right: "0", top: "0" }} /> */}
            <div ref={mountRef} style={{ width: "1200px", height: "800px" }} />
        </div>
    );
};

export default Viz;
