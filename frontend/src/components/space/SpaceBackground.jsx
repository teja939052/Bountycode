import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

function Particles({ count = 800 }) {
  const mesh = useRef();
  const light = useRef();

  const particles = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const sizes = new Float32Array(count);
    const speeds = new Float32Array(count);

    const palette = [
      [0.298, 0.788, 0.941],
      [0.447, 0.035, 0.718],
      [0.294, 0.710, 0.263],
    ];

    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 30;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 30;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20;

      const c = palette[Math.floor(Math.random() * palette.length)];
      colors[i * 3] = c[0];
      colors[i * 3 + 1] = c[1];
      colors[i * 3 + 2] = c[2];

      sizes[i] = Math.random() * 2 + 0.5;
      speeds[i] = Math.random() * 0.3 + 0.1;
    }

    return { positions, colors, sizes, speeds };
  }, [count]);

  useFrame((state) => {
    if (!mesh.current) return;
    const t = state.clock.elapsedTime;
    const pos = mesh.current.geometry.attributes.position.array;

    for (let i = 0; i < count; i++) {
      const speed = particles.speeds[i];
      pos[i * 3] += Math.sin(t * speed + i) * 0.001;
      pos[i * 3 + 1] += Math.cos(t * speed * 0.7 + i) * 0.001;
      pos[i * 3 + 2] += Math.sin(t * speed * 0.5 + i * 0.5) * 0.0005;
    }
    mesh.current.geometry.attributes.position.needsUpdate = true;

    if (light.current) {
      light.current.position.x = Math.sin(t * 0.3) * 5;
      light.current.position.y = Math.cos(t * 0.2) * 3;
    }
  });

  return (
    <>
      <pointLight ref={light} color="#4CC9F0" intensity={0.5} distance={20} />
      <points ref={mesh}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={particles.positions}
            count={count}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            array={particles.colors}
            count={count}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.04}
          vertexColors
          transparent
          opacity={0.6}
          sizeAttenuation
          blending={THREE.AdditiveBlending}
          depthWrite={false}
        />
      </points>
    </>
  );
}

export default function SpaceBackground() {
  return (
    <div className="fixed inset-0 z-0 pointer-events-none" style={{ opacity: 0.7 }}>
      <Canvas
        camera={{ position: [0, 0, 8], fov: 60 }}
        dpr={[1, 1.5]}
        gl={{ antialias: false, alpha: true }}
        style={{ background: "transparent" }}
      >
        <Particles count={600} />
      </Canvas>
    </div>
  );
}
