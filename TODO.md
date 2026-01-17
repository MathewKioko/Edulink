# EDULINK Customization Plan

## Information Gathered

### Current State Analysis
- **Project Name**: Group Connect (multiple variations: "GroupConnect", "Group-Connect")
- **Theme**: Basic Tailwind CSS with dark/light mode via Redux
- **Tech Stack**: React + TypeScript + Tailwind CSS + Vite + Redux + FastAPI + MongoDB
- **Current Branding**: Blue-purple gradient theme with "G" logo icon
- **GitHub References**: Points to nianod/Group-connect repository

### Files Requiring Changes
1. README.md - Main documentation
2. Clients/index.html - Title and favicon
3. Clients/package.json - Package name
4. Clients/src/Components/Layout/Header.tsx - Header branding
5. Clients/src/Components/Layout/Footer.tsx - Footer branding and links
6. Clients/src/Pages/Landing.tsx - Landing page content
7. Clients/src/Pages/Auth/SignIn.tsx - Sign in page branding
8. Clients/src/Pages/Auth/SignUp.tsx - Sign up page branding
9. Server/main.py - API title
10. Server/Routes/*.py - Route titles

---

## Plan: EDULINK Customization

### Phase 1: Branding Changes (Replace "Group Connect" → "EDULINK")
1. **Update README.md**
   - Change title from "Group Connect" to "EDULINK"
   - Update all descriptions and references
   - Add MathewKioko as developer
   - Update GitHub URL to new repository

2. **Update Frontend Files**
   - Clients/index.html: Change title to "EDULINK"
   - Clients/package.json: Change name to "edulink"
   - Clients/src/Components/Layout/Header.tsx: Update logo and title
   - Clients/src/Components/Layout/Footer.tsx: Update branding and social links
   - Clients/src/Pages/Landing.tsx: Update all text references
   - Clients/src/Pages/Auth/SignIn.tsx: Update branding
   - Clients/src/Pages/Auth/SignUp.tsx: Update branding

3. **Update Backend Files**
   - Server/main.py: Update API title
   - Update all route files with new references

### Phase 2: World-Class Theme Implementation
1. **Install shadcn/ui Components**
   - Install necessary dependencies (class-variance-authority, clsx, tailwind-merge)
   - Add utility functions for class merging
   - Create base component patterns

2. **Upgrade Color Scheme**
   - Professional education-focused colors (teal/blue/indigo)
   - Consistent gradient scheme across platform
   - Enhanced dark mode with better contrast

3. **Enhanced UI Components**
   - Professional button styles with hover effects
   - Improved form inputs
   - Better card components
   - Enhanced navigation with clear visual hierarchy

4. **Theme Store Improvements**
   - Enhanced theme preferences
   - Consistent color tokens
   - Better dark/light mode transitions

### Phase 3: GitHub & Developer Updates
1. **Update all GitHub links** to point to MathewKioko
2. **Add developer credits** throughout the application
3. **Update social media links** in footer
4. **Update package.json** repository field

### Phase 4: Documentation Updates
1. **Complete README overhaul** with new branding
2. **Add installation instructions** specific to EDULINK
3. **Update contributing guidelines** with MathewKioko as maintainer

---

## Dependent Files to be Edited

### Frontend (Clients/)
- [ ] README.md
- [ ] index.html
- [ ] package.json
- [ ] src/Components/Layout/Header.tsx
- [ ] src/Components/Layout/Footer.tsx
- [ ] src/Pages/Landing.tsx
- [ ] src/Pages/Auth/SignIn.tsx
- [ ] src/Pages/Auth/SignUp.tsx
- [ ] src/Components/Theme/store.ts
- [ ] src/Components/Theme/ThemeSlice.ts
- [ ] src/index.css

### Backend (Server/)
- [ ] main.py
- [ ] Routes/group.py
- [ ] Routes/user.py
- [ ] Routes/send.py

### Root
- [ ] README.md
- [ ] Clients/README.md

---

## Followup Steps

### Installation & Setup
1. Run `npm install` for Clients/
2. Run `pip install` for Server/
3. Set up MongoDB connection
4. Configure environment variables

### Testing
1. Verify all branding changes applied correctly
2. Test theme toggle functionality
3. Test all authentication flows
4. Verify responsive design
5. Check dark/light mode transitions

### Build & Deploy
1. Run production build for frontend
2. Test backend API endpoints
3. Deploy to appropriate hosting platforms
4. Update environment configurations

---

## Implementation Order

1. ✅ Phase 1: Branding Changes (High Priority)
2. 🔄 Phase 2: Theme Implementation (Medium Priority)
3. ⏳ Phase 3: GitHub Updates (Medium Priority)
4. ⏳ Phase 4: Documentation (Low Priority)

---

*Plan created: Ready for implementation*
*Estimated time: 2-3 hours for complete customization*

