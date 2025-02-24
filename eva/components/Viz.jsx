import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import styles from "./Viz.module.css";

export const Viz = () => {
    const mountRef = useRef(null);
    const [data, setData] = useState([]);

    useEffect(() => {
        if (!mountRef.current) return;

        // Scene, Camera, Renderer
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

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
        mountRef.current.appendChild(renderer.domElement);

        const ambientLight = new THREE.AmbientLight(0xffffff, 1);
        scene.add(ambientLight);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        // STL Loader
        let mesh;
        const loader = new STLLoader();
        loader.load(
            "/cubesat.stl",
            (geometry) => {
                const material = new THREE.MeshNormalMaterial({ wireframe: true });
                mesh = new THREE.Mesh(geometry, material);
                // mesh.scale.set(10, 10, 10);
                scene.add(mesh);
            },
            (xhr) => console.log((xhr.loaded / xhr.total) * 100 + "% loaded"),
            (error) => console.error("Error loading STL:", error)
        );

        const onWindowResize = () => {
            if (!mountRef.current) return;
            camera.aspect = mountRef.current.clientWidth / mountRef.current.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
        };
        window.addEventListener("resize", onWindowResize);

        const animate = () => {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };
        animate();

        // Simulated Data Updates for the Plot
        const interval = setInterval(() => {
            setData((prevData) => {
                const newData = [...prevData, { time: prevData.length, value: Math.random() * 10 }];
                return newData.length > 20 ? newData.slice(1) : newData; // Keep only 20 points
            });
        }, 500);

        return () => {
            window.removeEventListener("resize", onWindowResize);
            controls.dispose();
            renderer.dispose();
            clearInterval(interval);

            if (mesh) {
                mesh.geometry.dispose();
                mesh.material.dispose();
                scene.remove(mesh);
            }

            if (mountRef.current) {
                mountRef.current.removeChild(renderer.domElement);
            }
        };
    }, []);

    return (
        <div className={styles.container}>
            {/* 3D Viz */}
            <div ref={mountRef} className={styles.vizDiv} />

            {/* Video Feed */}
            <div className={styles.videoFeed}>
                <img src="http://192.168.223.236:5000/video_feed" alt="Stream" />
            </div>

            {/* Overlay Chart */}
            <div className={styles.chartOverlay}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data} title="a" margin={{ top: 30, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="1" />
                        <XAxis dataKey="time" />
                        <YAxis />
                        
                        {/* <Tooltip /> */}
                        <Line type="natural" dataKey="value" stroke="#8884d8" strokeWidth={2} dot={true} />
                    </LineChart>
                </ResponsiveContainer>
            </div>


            <div>
                
            </div>

            
        </div>
    );
};

export default Viz;

