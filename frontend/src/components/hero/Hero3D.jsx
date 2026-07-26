import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, MeshDistortMaterial } from "@react-three/drei";
import useReducedMotion from "../../hooks/useReducedMotion";

function ParticleSphere({ count = 200, color = "#818cf8" }) {
  const mesh = useRef();
  const reduced = useReducedMotion();

  const particles = useMemo(() => {
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = 3 + Math.random() * 2;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
    }
    return positions;
  }, [count]);

  useFrame((_, delta) => {
    if (!reduced && mesh.current) {
      mesh.current.rotation.y += delta * 0.15;
      mesh.current.rotation.x += delta * 0.05;
    }
  });

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={particles}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.04} color={color} transparent opacity={0.8} sizeAttenuation />
    </points>
  );
}

function GlowSphere() {
  const mesh = useRef();
  const reduced = useReducedMotion();

  useFrame((state) => {
    if (!reduced && mesh.current) {
      mesh.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime) * 0.1);
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.3} floatIntensity={0.5}>
      <mesh ref={mesh}>
        <sphereGeometry args={[1.2, 64, 64]} />
        <MeshDistortMaterial
          color="#6366f1"
          emissive="#4f46e5"
          emissiveIntensity={0.3}
          roughness={0.2}
          metalness={0.8}
          distort={0.3}
          speed={2}
          transparent
          opacity={0.7}
        />
      </mesh>
    </Float>
  );
}

function RingParticles() {
  const ring = useRef();
  const reduced = useReducedMotion();

  useFrame((_, delta) => {
    if (!reduced && ring.current) {
      ring.current.rotation.z += delta * 0.3;
    }
  });

  return (
    <mesh ref={ring} rotation={[Math.PI / 3, 0, 0]}>
      <torusGeometry args={[2.5, 0.02, 16, 100]} />
      <meshStandardMaterial color="#a78bfa" emissive="#8b5cf6" emissiveIntensity={0.5} transparent opacity={0.5} />
    </mesh>
  );
}

function Scene() {
  return (
    <>
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} intensity={1} color="#818cf8" />
      <pointLight position={[-10, -5, 5]} intensity={0.5} color="#c084fc" />
      <ParticleSphere count={300} color="#818cf8" />
      <GlowSphere />
      <RingParticles />
    </>
  );
}

export default function Hero3D() {
  const reduced = useReducedMotion();

  if (reduced) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <div className="w-32 h-32 rounded-full bg-primary-400/30 blur-2xl" />
      </div>
    );
  }

  return (
    <Canvas
      camera={{ position: [0, 0, 6], fov: 50 }}
      dpr={[1, 1.5]}
      gl={{ antialias: true, alpha: true }}
      style={{ background: "transparent" }}
    >
      <Scene />
    </Canvas>
  );
}
