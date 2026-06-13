# Paradise AI – Multi-Agent Investment Advisory System

## Overview

Paradise AI is an Agentic AI-powered Investment Advisory Platform that generates personalized investment strategies based on a user's financial profile, risk tolerance, investment horizon, and income.

The system uses a multi-agent architecture built with LangGraph, where specialized AI agents collaborate to analyze risk, create portfolio allocations, simulate market conditions, verify compliance, critique recommendations, and explain decisions in a transparent manner.

---

## Features

### Multi-Agent Workflow
- Profile Analysis Agent
- Investment Strategy Agent
- Market Simulation Agent
- Compliance Verification Agent
- Critic & Validation Agent
- Explanation Agent

### Intelligent Risk Assessment
Calculates a personalized risk score using:
- Age
- Income
- Investment Horizon
- Loss Tolerance

### Portfolio Allocation
Generates investment allocations across asset classes based on risk appetite.

### Market Stress Testing
Simulates different market scenarios to evaluate portfolio robustness.

### Compliance-Aware Recommendations
Validates recommendations against investment guidelines using a RAG-powered compliance system.

### Explainable AI
Provides human-readable explanations for every recommendation.

### User Authentication
- Registration
- Login
- Session Management

---

## Architecture

```text
User Profile
      │
      ▼
Profile Agent
      │
      ▼
Strategy Agent
      │
      ▼
Simulation Agent
      │
      ▼
Compliance Agent
      │
      ▼
Critic Agent
      │
      ├── Retry Required
      │       │
      │       ▼
      │   Strategy Agent
      │
      ▼
Explanation Agent
      │
      ▼
Final Recommendation
