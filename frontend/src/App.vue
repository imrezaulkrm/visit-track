<template>
    <div class="app">
        <canvas ref="bgCanvas" class="background-canvas"></canvas>

        <div class="content">
            <h1 class="title">Visitors</h1>
            <div class="stats-card">
                <div class="stat">
                    <div class="label">Total Visitors</div>
                    <div class="value">{{ totalVisits }}</div>
                </div>
                <div class="stat">
                    <div class="label">Live Visitors</div>
                    <div class="value live">{{ liveVisitors }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const totalVisits = ref(0);
const liveVisitors = ref(0);

const BASE_API = 'http://127.0.0.1:8000/visitors';

// For Canvas animation
const bgCanvas = ref(null);
let ctx = null;
let animationFrameId = null;
const particles = [];
const PARTICLE_COUNT = 60;

function random(min, max) {
    return Math.random() * (max - min) + min;
}

// Particle class
class Particle {
    constructor(width, height) {
        this.x = random(0, width);
        this.y = random(0, height);
        this.size = random(1, 3);
        this.speedX = random(-0.3, 0.3);
        this.speedY = random(-0.3, 0.3);
        this.color = 'rgba(0, 200, 255, 0.5)';
    }
    update(width, height) {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x < 0 || this.x > width) this.speedX *= -1;
        if (this.y < 0 || this.y > height) this.speedY *= -1;
    }
    draw(ctx) {
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.shadowColor = 'rgba(0, 200, 255, 0.3)';
        ctx.shadowBlur = 5;
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function initParticles(width, height) {
    particles.length = 0;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push(new Particle(width, height));
    }
}

function animateCanvas(width, height) {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
        let p1 = particles[i];
        p1.draw(ctx);

        for (let j = i + 1; j < particles.length; j++) {
            let p2 = particles[j];
            let dx = p1.x - p2.x;
            let dy = p1.y - p2.y;
            let dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 120) {
                ctx.beginPath();
                ctx.strokeStyle = `rgba(0, 200, 255, ${1 - dist / 120})`;
                ctx.lineWidth = 1;
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        }
    }

    // Update particle positions
    particles.forEach((p) => p.update(width, height));

    animationFrameId = requestAnimationFrame(() =>
        animateCanvas(width, height)
    );
}

async function trackVisitor() {
    try {
        await fetch(`${BASE_API}/track/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (e) {
        console.error('Track visitor failed:', e);
    }
}

async function fetchStats() {
    try {
        const res = await fetch(`${BASE_API}/stats/`);
        if (!res.ok) throw new Error('Failed to fetch stats');
        const data = await res.json();
        totalVisits.value = data.total_visits;
        liveVisitors.value = data.live_visitors;
    } catch (e) {
        console.error('Fetch stats failed:', e);
    }
}

onMounted(() => {
    const canvas = bgCanvas.value;
    ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    initParticles(canvas.width, canvas.height);
    animateCanvas(canvas.width, canvas.height);

    trackVisitor();
    fetchStats();
    setInterval(fetchStats, 5000);

    onBeforeUnmount(() => {
        cancelAnimationFrame(animationFrameId);
        window.removeEventListener('resize', resizeCanvas);
    });
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.app {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #001a26;
    color: #00c8ff;
    font-family: 'Roboto', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
}

.background-canvas {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 0;
    width: 100vw;
    height: 100vh;
    background: #001a26;
}

.content {
    position: relative;
    z-index: 10;
    text-align: center;
    width: 30%;
    padding: 2.5rem 3rem;
    background: rgba(0, 0, 0, 0.35);
    border-radius: 16px;
    box-shadow: 0 0 10px rgba(0, 200, 255, 0.3);
}

h1.title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 2.8rem;
    color: rgb(255, 255, 255);
    user-select: none;
    text-shadow: 0 0 20px rgba(0, 200, 255, 0.7);
}

.stats-card {
    font-weight: 700;
    letter-spacing: 1.7px;
}

.stat {
    margin-bottom: 2rem;
}

.label {
    font-size: 1.15rem;
    color: #ffffff;
    margin-bottom: 0.5rem;
    user-select: none;
}

.value {
    font-size: 3.5rem;
    color: #72f549;
    user-select: none;
    text-shadow: none;
}

.value.live {
    color: #ff4777;
    text-shadow: none;
}
</style>
