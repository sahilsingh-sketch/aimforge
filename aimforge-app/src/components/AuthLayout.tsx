import { useEffect, useRef, type ReactNode } from 'react';
import * as THREE from 'three';
import '../pages/Auth.css';

interface AuthLayoutProps {
  children: ReactNode;
}

export function AuthLayout({ children }: AuthLayoutProps) {
  const stageRef = useRef<HTMLDivElement>(null);
  const heroRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!stageRef.current || !heroRef.current) return;

    const stageEl = stageRef.current;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 0, 7.2);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    stageEl.appendChild(renderer.domElement);

    const orangeMain = 0xff5d1f;
    const orangeLight = 0xff9152;
    const orangeDim = 0x7a3417;

    const group = new THREE.Group();
    scene.add(group);

    // Core wireframe icosahedron
    const coreGeo = new THREE.IcosahedronGeometry(1.05, 1);
    const coreMat = new THREE.MeshBasicMaterial({ color: orangeMain, wireframe: true, transparent: true, opacity: 0.85 });
    const core = new THREE.Mesh(coreGeo, coreMat);
    group.add(core);

    // Soft inner glow sphere
    const glowGeo = new THREE.SphereGeometry(0.62, 24, 24);
    const glowMat = new THREE.MeshBasicMaterial({ color: orangeMain, transparent: true, opacity: 0.22 });
    const glow = new THREE.Mesh(glowGeo, glowMat);
    group.add(glow);

    // Target rings (torus)
    const ringDefs = [
      { r: 1.9, tube: 0.014, color: orangeMain, rotX: Math.PI / 2.1, rotY: 0.15, opacity: 0.75, speed: 0.35 },
      { r: 2.35, tube: 0.010, color: orangeLight, rotX: Math.PI / 2 + 0.5, rotY: -0.4, opacity: 0.42, speed: -0.22 },
      { r: 2.75, tube: 0.008, color: orangeDim, rotX: Math.PI / 2 - 0.35, rotY: 0.9, opacity: 0.3, speed: 0.15 },
    ];
    
    const rings = ringDefs.map(def => {
      const geo = new THREE.TorusGeometry(def.r, def.tube, 8, 96);
      const mat = new THREE.MeshBasicMaterial({ color: def.color, transparent: true, opacity: def.opacity });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.rotation.x = def.rotX;
      mesh.rotation.y = def.rotY;
      mesh.userData = { speed: def.speed };
      group.add(mesh);
      return mesh;
    });

    // Crosshair lines
    function makeLine(points: THREE.Vector3[], color: number, opacity: number) {
      const geo = new THREE.BufferGeometry().setFromPoints(points);
      const mat = new THREE.LineBasicMaterial({ color, transparent: true, opacity });
      return new THREE.Line(geo, mat);
    }
    const crossGroup = new THREE.Group();
    crossGroup.add(makeLine([new THREE.Vector3(-3.1, 0, 0), new THREE.Vector3(3.1, 0, 0)], orangeMain, 0.28));
    crossGroup.add(makeLine([new THREE.Vector3(0, -3.1, 0), new THREE.Vector3(0, 3.1, 0)], orangeMain, 0.28));
    group.add(crossGroup);

    // Particle field
    const particleCount = 140;
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
      const radius = 4.2 + Math.random() * 2.4;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);
      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi) * 0.4;
    }
    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const particleMat = new THREE.PointsMaterial({ color: orangeLight, size: 0.025, transparent: true, opacity: 0.5 });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // Resize handling
    const resize = () => {
      if (!stageEl) return;
      const w = stageEl.clientWidth;
      const h = stageEl.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', resize);
    resize();

    // Mouse parallax
    let mouseX = 0, mouseY = 0, targetX = 0, targetY = 0;
    const handleMouseMove = (e: MouseEvent) => {
      const r = stageEl.getBoundingClientRect();
      mouseX = ((e.clientX - r.left) / r.width - 0.5) * 2;
      mouseY = ((e.clientY - r.top) / r.height - 0.5) * 2;
    };
    heroRef.current.addEventListener('mousemove', handleMouseMove);

    const clock = new THREE.Clock();
    let animationId: number;

    const animate = () => {
      animationId = requestAnimationFrame(animate);
      const t = clock.getElapsedTime();

      targetX += (mouseX - targetX) * 0.04;
      targetY += (mouseY - targetY) * 0.04;

      group.rotation.y = t * 0.12 + targetX * 0.35;
      group.rotation.x = targetY * 0.25 + Math.sin(t * 0.3) * 0.03;

      rings.forEach((mesh) => {
        mesh.rotation.z += 0.0025 * ((mesh.userData.speed as number) / 0.25);
      });

      core.rotation.x += 0.0015;
      core.rotation.y += 0.0022;

      const pulse = 1 + Math.sin(t * 1.6) * 0.03;
      glow.scale.setScalar(pulse);

      particles.rotation.y = t * 0.02;

      // Lock-on animation (handled via a global state/class in React if needed)
      if (document.body.classList.contains('is-locking')) {
         // Simplify lock-on for now in React by just scaling down
         rings.forEach((mesh) => mesh.scale.setScalar(0.7));
      } else {
         rings.forEach((mesh) => mesh.scale.setScalar(1));
      }

      renderer.render(scene, camera);
    };
    animate();

    return () => {
      window.removeEventListener('resize', resize);
      if (heroRef.current) heroRef.current.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationId);
      stageEl.removeChild(renderer.domElement);
      
      coreGeo.dispose();
      coreMat.dispose();
      glowGeo.dispose();
      glowMat.dispose();
      particleGeo.dispose();
      particleMat.dispose();
    };
  }, []);

  return (
    <div className="auth-layout">
      <div className="auth-shell">
        <div className="auth-frame">
          <div className="auth-hero" id="hero" ref={heroRef}>
            <div className="auth-brand">
              <div className="brand-mark">
                <svg viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="9" stroke="#0A0704" strokeWidth="1.6" />
                  <circle cx="12" cy="12" r="2.6" fill="#0A0704" />
                  <path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke="#0A0704" strokeWidth="1.6" strokeLinecap="round" />
                </svg>
              </div>
              <div className="brand-text">
                <span className="brand-name">AimForge<span className="lit"></span></span>
                <span className="brand-sub">AI-powered gameplay analysis</span>
              </div>
            </div>

            <div className="auth-stage" id="stage" ref={stageRef}>
              <div className="hero-vignette"></div>
              <div className="auth-chip tl">
                <span className="dot"></span>PRECISION
              </div>
              <div className="auth-chip br">RANK UP &rarr;</div>
            </div>

            <div className="hero-copy">
              <div className="auth-eyebrow">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L4 6v6c0 5 3.4 8.7 8 10 4.6-1.3 8-5 8-10V6l-8-4z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
                </svg>
                FORGE YOUR ADVANTAGE
              </div>
              <h1 className="auth-headline">Your next level starts with better decisions.</h1>
              <p className="auth-subcopy">
                Review every replay, understand every mistake, and train with a coach that knows your gameplay.
              </p>
              <div className="feature-row">
                <div className="auth-feature">
                  <svg viewBox="0 0 24 24" fill="none">
                    <rect x="4" y="10" width="16" height="10" rx="2" stroke="currentColor" strokeWidth="1.6" />
                    <path d="M8 10V7a4 4 0 018 0v3" stroke="currentColor" strokeWidth="1.6" />
                  </svg>
                  Private by design
                </div>
                <div className="auth-feature">
                  <svg viewBox="0 0 24 24" fill="none">
                    <path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
                  </svg>
                  Instant insights
                </div>
              </div>
            </div>
          </div>

          <div className="auth-panel">
             {children}
          </div>
        </div>
      </div>
    </div>
  );
}
