#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}       Project Framework - New Project Setup       ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

validate_kebab_case() {
    if [[ ! "$1" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        echo -e "${RED}Error: Name must be in kebab-case (e.g., 'api-migration', 'fix-auth-bug')${NC}"
        return 1
    fi
    return 0
}

echo -e "${YELLOW}Let's set up your new project. I'll ask a few questions.${NC}"
echo ""

while true; do
    read -p "$(echo -e ${GREEN}Project name ${NC}${YELLOW}[kebab-case]${NC}: )" PROJECT_NAME
    if validate_kebab_case "$PROJECT_NAME"; then
        break
    fi
done

read -p "$(echo -e ${GREEN}Brief description ${NC}${YELLOW}[1-2 sentences]${NC}: )" PROJECT_DESC
read -p "$(echo -e ${GREEN}Primary goal${NC}: )" PROJECT_GOAL
read -p "$(echo -e ${GREEN}Target timeline ${NC}${YELLOW}[e.g., '1 week', '2 weeks']${NC}: )" PROJECT_TIMELINE
read -p "$(echo -e ${GREEN}Technology stack ${NC}${YELLOW}[e.g., 'Python/FastAPI', 'TypeScript/React']${NC}: )" PROJECT_TECH

echo ""
echo -e "${YELLOW}Project type options:${NC}"
echo "  1) feature-development"
echo "  2) refactoring"
echo "  3) migration"
echo "  4) bug-fix"
echo "  5) optimization"
echo "  6) research"
echo "  7) other"
echo ""

while true; do
    read -p "$(echo -e ${GREEN}Project type ${NC}${YELLOW}[1-7]${NC}: )" TYPE_NUM
    case $TYPE_NUM in
        1) PROJECT_TYPE="feature-development"; break;;
        2) PROJECT_TYPE="refactoring"; break;;
        3) PROJECT_TYPE="migration"; break;;
        4) PROJECT_TYPE="bug-fix"; break;;
        5) PROJECT_TYPE="optimization"; break;;
        6) PROJECT_TYPE="research"; break;;
        7) PROJECT_TYPE="other"; break;;
        *) echo -e "${RED}Please enter a number 1-7${NC}";;
    esac
done

read -p "$(echo -e ${GREEN}Affected components ${NC}${YELLOW}[e.g., 'backend services', 'frontend']${NC}: )" PROJECT_COMPONENTS
read -p "$(echo -e ${GREEN}Dependencies ${NC}${YELLOW}[optional, press Enter for none]${NC}: )" PROJECT_DEPS
read -p "$(echo -e ${GREEN}Success criteria ${NC}${YELLOW}[comma-separated]${NC}: )" PROJECT_SUCCESS
read -p "$(echo -e ${GREEN}Known risks ${NC}${YELLOW}[optional, press Enter for none]${NC}: )" PROJECT_RISKS

PROJECT_DEPS="${PROJECT_DEPS:-None}"
PROJECT_RISKS="${PROJECT_RISKS:-None}"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                   Summary                        ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "  Name:       ${GREEN}${PROJECT_NAME}${NC}"
echo -e "  Goal:       ${PROJECT_GOAL}"
echo -e "  Timeline:   ${PROJECT_TIMELINE}"
echo -e "  Tech:       ${PROJECT_TECH}"
echo -e "  Type:       ${PROJECT_TYPE}"
echo -e "  Components: ${PROJECT_COMPONENTS}"
echo ""

read -p "$(echo -e ${YELLOW}Proceed with project creation? ${NC}${GREEN}[Y/n]${NC}: )" CONFIRM
CONFIRM="${CONFIRM:-Y}"

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Project creation cancelled.${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}Creating project...${NC}"

python3 "${REPO_ROOT}/_projects/_scripts/bootstrap_project.py" \
    --name "$PROJECT_NAME" \
    --description "$PROJECT_DESC" \
    --goal "$PROJECT_GOAL" \
    --timeline "$PROJECT_TIMELINE" \
    --tech "$PROJECT_TECH" \
    --type "$PROJECT_TYPE" \
    --components "$PROJECT_COMPONENTS" \
    --dependencies "$PROJECT_DEPS" \
    --success-criteria "$PROJECT_SUCCESS" \
    --risks "$PROJECT_RISKS"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              Project Created!                    ${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "  To resume in any future session:"
echo -e "  ${YELLOW}Drag the next-task.md file into your Cursor chat${NC}"
echo ""
