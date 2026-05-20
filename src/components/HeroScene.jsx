import { useEffect, useRef } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import combinedModelUrl from "../../models/pot_vase_and_base.glb?url";

function makeNoiseTexture({
  base = [190, 127, 70],
  speck = [75, 42, 24],
  size = 256,
  speckles = 1300,
} = {}) {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  const gradient = ctx.createLinearGradient(0, 0, size, size);
  gradient.addColorStop(0, `rgb(${base[0] + 32}, ${base[1] + 28}, ${base[2] + 22})`);
  gradient.addColorStop(0.72, `rgb(${base[0]}, ${base[1]}, ${base[2]})`);
  gradient.addColorStop(1, `rgb(${base[0] - 32}, ${base[1] - 28}, ${base[2] - 18})`);
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);

  for (let i = 0; i < speckles; i += 1) {
    const alpha = Math.random() * 0.22 + 0.04;
    const radius = Math.random() * 1.7 + 0.35;
    ctx.fillStyle = `rgba(${speck[0]}, ${speck[1]}, ${speck[2]}, ${alpha})`;
    ctx.beginPath();
    ctx.arc(Math.random() * size, Math.random() * size, radius, 0, Math.PI * 2);
    ctx.fill();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2.4, 2.4);
  return texture;
}

function clayMaterial(texture) {
  return new THREE.MeshStandardMaterial({
    map: texture,
    color: "#d49a67",
    roughness: 0.96,
    metalness: 0,
  });
}

function baseMaterial(texture) {
  return new THREE.MeshStandardMaterial({
    map: texture,
    color: "#b87a48",
    roughness: 0.98,
    metalness: 0,
  });
}

function plantMaterial() {
  return new THREE.MeshStandardMaterial({
    color: "#8b5a31",
    roughness: 0.92,
    metalness: 0,
  });
}

function budMaterial() {
  return new THREE.MeshStandardMaterial({
    color: "#c99044",
    roughness: 0.95,
    metalness: 0,
  });
}

export default function HeroScene() {
  const mountRef = useRef(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return undefined;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(28, 1, 0.1, 100);
    camera.position.set(0.2, 0.44, 6.1);
    camera.lookAt(0, 0.24, 0);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0xffffff, 0);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mount.appendChild(renderer.domElement);

    const group = new THREE.Group();
    group.position.set(0.48, -0.28, 0);
    group.rotation.y = -0.12;
    scene.add(group);

    const clayTex = makeNoiseTexture();
    const baseTex = makeNoiseTexture({
      base: [154, 94, 52],
      speck: [64, 35, 20],
      speckles: 2600,
    });
    const vaseMat = clayMaterial(clayTex);
    const roughBaseMat = baseMaterial(baseTex);
    const twigMat = plantMaterial();
    const driedBudMat = budMaterial();
    const mouthMat = new THREE.MeshStandardMaterial({
      color: "#2a150c",
      roughness: 0.98,
      metalness: 0,
    });

    const shadowPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(6, 4),
      new THREE.ShadowMaterial({ color: "#5a2b18", opacity: 0.14 }),
    );
    shadowPlane.rotation.x = -Math.PI / 2;
    shadowPlane.position.set(0, -1.21, 0);
    shadowPlane.receiveShadow = true;
    group.add(shadowPlane);

    const loader = new GLTFLoader();
    const loaded = [];
    let disposed = false;

    function applyMaterials(root, kind) {
      root.traverse((child) => {
        if (!child.isMesh) return;
        child.castShadow = true;
        child.receiveShadow = true;
        const name = child.material?.name || "";
        const objectName = child.name || "";
        if (kind === "base" || name.includes("Base") || objectName.includes("Base")) {
          child.material = roughBaseMat;
        } else if (name.includes("Stem") || name.includes("Twig")) {
          child.material = twigMat;
        } else if (name.includes("Bud")) {
          child.material = driedBudMat;
        } else if (name.includes("Mouth")) {
          child.material = mouthMat;
        } else {
          child.material = vaseMat;
        }
      });
    }

    function fitLoadedScene(root) {
      root.traverse((child) => {
        if (child.isMesh && child.name.includes("Base")) {
          child.scale.set(0.72, 0.68, 0.72);
        }
      });

      root.updateMatrixWorld(true);
      const box = new THREE.Box3().setFromObject(root);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      root.position.sub(center);

      const maxDimension = Math.max(size.x, size.y, size.z);
      const scale = maxDimension > 0 ? 3.1 / maxDimension : 1;
      root.scale.setScalar(scale);

      root.updateMatrixWorld(true);
      const fittedBox = new THREE.Box3().setFromObject(root);
      const fittedCenter = fittedBox.getCenter(new THREE.Vector3());
      const fittedSize = fittedBox.getSize(new THREE.Vector3());
      root.position.x -= fittedCenter.x;
      root.position.y -= fittedCenter.y - 0.12;
      root.position.z -= fittedCenter.z;

      camera.position.set(0.2, 0.44, 6.1);
      camera.lookAt(0, 0.24, 0);
      shadowPlane.position.y = -fittedSize.y * 0.5 - 0.02;
    }

    loader.load(
      combinedModelUrl,
      (gltf) => {
        if (disposed) return;
        applyMaterials(gltf.scene, "combined");
        fitLoadedScene(gltf.scene);
        group.add(gltf.scene);
        loaded.push(gltf.scene);
      },
      undefined,
      (error) => {
        console.error("Failed to load hero GLB model", error);
      },
    );

    const key = new THREE.DirectionalLight("#fff0dd", 3.2);
    key.position.set(3.2, 3.8, 4.5);
    key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    key.shadow.camera.near = 0.5;
    key.shadow.camera.far = 12;
    key.shadow.camera.left = -4;
    key.shadow.camera.right = 4;
    key.shadow.camera.top = 4;
    key.shadow.camera.bottom = -4;
    scene.add(key);

    const fill = new THREE.HemisphereLight("#fff5e8", "#c7835b", 1.35);
    scene.add(fill);

    const warmSide = new THREE.PointLight("#e39a5d", 1.1, 7);
    warmSide.position.set(-3, 0.2, 2);
    scene.add(warmSide);

    function resize() {
      const rect = mount.getBoundingClientRect();
      const width = Math.max(1, Math.round(rect.width));
      const height = Math.max(1, Math.round(rect.height));
      camera.aspect = width / height;
      camera.lookAt(0, 0.24, 0);
      camera.updateProjectionMatrix();
      renderer.setSize(width, height, false);
    }

    function animate() {
      renderer.render(scene, camera);
    }

    resize();
    renderer.setAnimationLoop(animate);
    window.addEventListener("resize", resize);

    return () => {
      disposed = true;
      window.removeEventListener("resize", resize);
      renderer.setAnimationLoop(null);
      mount.removeChild(renderer.domElement);
      loaded.forEach((root) => group.remove(root));
      renderer.dispose();
      clayTex.dispose();
      baseTex.dispose();
      vaseMat.dispose();
      roughBaseMat.dispose();
      twigMat.dispose();
      driedBudMat.dispose();
      mouthMat.dispose();
      shadowPlane.geometry.dispose();
      shadowPlane.material.dispose();
    };
  }, []);

  return <div className="hero-scene" ref={mountRef} />;
}
