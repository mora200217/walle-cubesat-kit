
"use client"
import { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";

import styles from "./Viz.module.css";
import { SideBar } from "./SideBar/SideBar";
import { Title } from './AppTitle/Title';
import GUI from 'lil-gui'; 



export const Viz = () => {
    const gui = new GUI();

    let sensorData; 
    let angles = new Array(10).fill(0); 
    const mountRef = useRef(null);
    const [data, setData] = useState([]);

    const [messages, setMessages] = useState([]);
    const [ws, setWs] = useState(null);
  
    useEffect(() => {
      const socket = new WebSocket("ws://192.168.30.236:8080");
  
      socket.onopen = () => {
        console.log("Connected to WebSocket server");
        socket.send(JSON.stringify({ action: "ping" }));
      };
  
      socket.onmessage = (event) => {
        console.log(event)
        sensorData = JSON.parse(event.data);
        console.log(data)
        
      };
  
      socket.onclose = () => console.log("WebSocket disconnected");
  
      setWs(socket);
  
      return () => socket.close();
    }, []);
  
    const sendMessage = () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ message: "Hello from client" }));
      }
    };

    

    useEffect(() => {

        let  mesh; 
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
        // var mesh;
        const loader = new STLLoader();
        loader.load(
            "/cubesat.stl",
            (geometry) => {
                const material = new THREE.MeshNormalMaterial({ wireframe: true, depthFunc: true, depthWrite: true});
                let center = new THREE.Vector3();

                mesh = new THREE.Mesh(geometry, material);
                geometry.translate(-0.05, -0.1, -0.05);
                mesh.scale.set(10, 10, 10);
                
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
        controls.autoRotate = false;
        camera.position.y = 2; 
        console.log()
        


        const animate = () => {
            
            if (mesh) {

                mesh.rotation.x = sensorData.pitch / 180 * Math.PI; 
                mesh.rotation.y = sensorData.roll / 180 * Math.PI; 
            }

            
            controls.target.set(0,0,0)
            requestAnimationFrame(animate);
            // mesh.rotation.y += 2; 
            controls.update();
            renderer.render(scene, camera);
        };
        animate();

        // Simulated Data Updates for the Plot
        const interval = setInterval(() => {
            setData((prevData) => {
                const newData = [...prevData, { time: prevData.length, value: sensorData.pitch }];
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
                
                <img 
                    src="http://192.168.30.236:5000/video_feed"
                     alt="Video Stream" 
                    //  onError={(e)=> {e.target.src}}
                />
                <h6>Video Feed</h6>
            </div>

            {/* Overlay Chart */}
            <SideBar>
                
            </SideBar>
           
            <Title/>

            <div>
                
            </div>

            
        </div>
    );
};

export default Viz;

