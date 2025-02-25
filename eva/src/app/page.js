"use client"

import Image from "next/image";
import styles from "./page.module.css";
import { Viz } from '../../components/Viz';

import * as THREE from 'three';
import { Title } from '../../components/AppTitle/Title';
import { FooterContainer } from '../../components/FooterContainer/FooterContainer';
import { SideBar } from "../../components/SideBar/SideBar";

export default function Home() {


  return (
    <div className={styles.page}>
      

      <main className={styles.main}>
      
        <div>
          
          <Title />
          <Viz/>
        </div>
      </main>
    <FooterContainer />
    </div>
  );
}
